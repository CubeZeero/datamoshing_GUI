import os
import subprocess
import json
import numpy
import time

def get_vectors(input_video):
    # extract video data using ffedit
    subprocess.call(f'ffgac -i {input_video} -an -mpv_flags +nopimb+forcemv -qscale:v 0 -g 1000' +
                    ' -vcodec mpeg2video -f rawvideo -y tmp.mpg', shell=True)
    subprocess.call(f'ffedit -i tmp.mpg -f mv:0 -e tmp.json', shell=True)
    os.remove('tmp.mpg')

    # read the data we extracted
    f = open('tmp.json', 'r')
    raw_data = json.load(f)
    f.close()
    os.remove('tmp.json')

    # read frame information
    frames = raw_data['streams'][0]['frames']

    # get vectors from each frame
    vectors = []
    for frame in frames:
        try:
            vectors.append(frame['mv']['forward'])
        except:
            vectors.append([])

    return vectors


def apply_vectors(vectors, input_video, output_video, method='add'):
    subprocess.call(f'ffgac -i {input_video} -an -mpv_flags +nopimb+forcemv -qscale:v 0 -g 1000' +
                    ' -vcodec mpeg2video -f rawvideo -y tmp.mpg', shell=True)

    # open js file and read its contents
    to_add = '+' if method == 'add' else ''
    script_contents = '''
    var vectors = [];
    var n_frames = 0;

    function glitch_frame(frame) {
        let fwd_mvs = frame["mv"]["forward"];
        if (!fwd_mvs || !vectors[n_frames]) {
            n_frames++;
            return;
        }

        for ( let i = 0; i < fwd_mvs.length; i++ ) {
            let row = fwd_mvs[i];
            for ( let j = 0; j < row.length; j++ ) {
                let mv = row[j];
                try {
                    mv[0] ''' + to_add + '''= vectors[n_frames][i][j][0];
                    mv[1] ''' + to_add + '''= vectors[n_frames][i][j][1];
                } catch {}
            }
        }

        n_frames++;
    }
    '''

    script_path = 'apply_vectors.js'

    # open js file and write the code
    with open(script_path, 'w') as f:
        f.write(script_contents.replace('var vectors = [];', f'var vectors = {json.dumps(vectors)};'))

    # apply the effect
    subprocess.call(f'ffedit -i tmp.mpg -f mv -s {script_path} -o vector_tmp.mp4', shell=True)
    subprocess.call(f'ffmpeg -y -i vector_tmp.mp4 {output_video}', shell=True)

    # remove temp files
    os.remove('apply_vectors.js')
    os.remove('tmp.mpg')
    os.remove('vector_tmp.mp4')

    print('video glitch successfully.')
    time.sleep(1)
