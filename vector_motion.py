#!/usr/bin/env python3

import argparse
import subprocess
import os
import importlib.util as imp
from vector_util import get_vectors, apply_vectors
import sys
import numpy
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_video', type=str, help='specifies input file')
    parser.add_argument('-s', type=str, dest='script_path', help='path to the script', required=True)
    parser.add_argument('-g', type=str, default=1000, dest='gop_period', help='I-frame period (in frames)')
    parser.add_argument('-o', default='moshed.mp4', type=str, dest='output_video',
                        help='output file for the moshed video')
    return parser.parse_args().__dict__


def get_moshing_function(path):
    spec = imp.spec_from_file_location('mod', path)
    mod = imp.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.mosh_frames


if __name__ == '__main__':
    args = parse_args()
    input_video = args['input_video']
    gop_period = args['gop_period']
    output_video = args['output_video']
    script_path = args['script_path']
    script_type = script_path[-2:]

    if script_type == 'py':
        try:
            # import the function responsible for moshing from the specified script
            func = get_moshing_function(script_path)

            # method = '' specifies to just copy the new vectors over to the original video
            apply_vectors(func(get_vectors(input_video)), input_video, output_video, method='')
        except Exception as e:
            # TODO: proper error handling
            print(f'couldn\'t apply function mosh_frames from script: {script_path}:\n{e}')
            sys.exit()
    else:
        subprocess.call(f'ffgac -i {input_video} -an -mpv_flags +nopimb+forcemv -qscale:v 0 -g {gop_period}' +
                        ' -vcodec mpeg2video -f rawvideo -y tmp.mpg', shell=True)

        subprocess.call(f'ffedit -i tmp.mpg -f mv -s {script_path} -o vector_tmp.mp4', shell=True)
        subprocess.call(f'ffmpeg -y -i vector_tmp.mp4 {output_video}', shell=True)

        # remove temp files
        os.remove('tmp.mpg')
        os.remove('vector_tmp.mp4')

        print('video glitch successfully.')
        time.sleep(1)
