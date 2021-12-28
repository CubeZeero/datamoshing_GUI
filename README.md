# Datamoshing_GUI

![](https://i.imgur.com/X65KI8L.png)

Datamoshing made easy. 

This repository is a forked version of the [Tiberiu Iancu's datamoshing repository](https://github.com/tiberiuiancu/datamoshing), modified to be GUI-based and easier to use.

I would like to thank you [Tiberiu Iancu](https://github.com/tiberiuiancu) for creating such a wonderful project.

## Requirements

You will need `ffmpeg`, `ffedit`, and `ffgac` to run this script.

`ffedit` and `ffgac` are distributed as ffglitch.

**ffmpeg**

[.windows download (ffmpeg-nx.x-latest-win64-gpl-shared-x.x.zip)](https://github.com/BtbN/FFmpeg-Builds/releases)

.MacOS use homebrew `brew install ffmpeg`

.Linux use apt `sudo apt install ffmpeg`

**ffglitch**

[ffglitch download (stable ver0.9.3)](https://ffglitch.org/pub/bin/win64/ffglitch-0.9.3-win64.7z)

**Important:**
`After downloading, you will need to set the Path environment variable`

## Download

Please download it from the [release page.](https://github.com/CubeZeero/datamoshing_GUI/releases/tag/v1.0)

# Effects

## ffmpeg_datamosh

The following settings are available in ffmpeg_datamosh.

| Command | Description | Required |
| ------- | ----------- | -------- |
| `Input` | Input mp4 file | Yes |
| `Output` | Output file for the moshed video | No |
| `Startframe` | Start frame of the mosh | No |
| `Endframe` | End frame of the mosh | No |
| `FPS` | FPS to convert initial video to | No |
| `Delta` | Number of delta frames to repeat | No |

### i-frame removal
This type of glitch creates the transition effect. Example:

| Original | Moshed |
|:--------:|:------:|
| ![original_hand](https://user-images.githubusercontent.com/31802439/112060042-f3e42780-8b5c-11eb-8019-df4d06dd0d31.gif) | ![moshed_hand](https://user-images.githubusercontent.com/31802439/112060033-f181cd80-8b5c-11eb-9025-65064bbc6200.gif) |

| Command | Description |
| ------- | ----------- |
| `Input` | input.mp4 |
| `Output` | output.mp4 |
| `Startframe` | 40 |
| `Endframe` | 90 |

    $ ffmpeg_datamosh.exe input.mp4 -s 40 -e 90 -o output.mp4
    
removes all the i-frames from the input video starting at frame 40 and ending at frame 90, and outputs the final result
to `output.mp4`

### p-frame duplication
Repeats a series of p-frames (aka delta frames), which can give a 'melting' effect. This type of glitch is triggered by the `-d` flag. Example:

| Original | Moshed |
|:--------:|:------:|
| ![original_dog](https://user-images.githubusercontent.com/31802439/112059335-0316a580-8b5c-11eb-98c8-3493969dd472.gif) | ![moshed_dog](https://user-images.githubusercontent.com/31802439/112060106-065e6100-8b5d-11eb-9670-4ad3bd9522cd.gif) |

| Command | Description |
| ------- | ----------- |
| `Input` | dog.mp4 |
| `Output` | moshed_dog.mp4 |
| `Startframe` | 165 |
| `Delta` | 5 |

    $ ffmpeg_datamosh.exe dog.mp4 -d 5 -s 165 -o moshed_dog.mp4

copies 5 frames starting at frame 165, then replaces all subsequent groups of 5 frames with the copied data (in this case until the video ends, as no `-e` flag was specified).

## Vector motion

The following settings are available in VectorMotion.

| Command | Description | Required |
| ------- | ----------- | -------- |
| `Input` | Input mp4 file | Yes |
| `Output` | Output file for the moshed video | No |
| `Script` | path to the script | Yes |
| `I-frame period (in frames)` | I-frame period (in frames) | No |

While the previous effects copy and delete whole frames, this one changes the actual frame data. As explained in
[this article on ffglitch.org](https://ffglitch.org/2020/07/mv.html), you need to write a custom JavaScript file
that can change the frame data. `vector_motion.py` is just a wrapper for `ffedit` and `ffgac` and makes moshing
possible through only one command.
Example:

    $ vector_motion.exe input.mp4 -s your_script.js -o output.mp4

### Now also with Python!

If you prefer to use python to glitch the frames instead, you can also specify a python script for the `-s` option.
The script must contain a function called `mosh_frames` that takes as argument an array of frames (warning: some of the frames
might be empty), where each non-empty frame represents a 3D array of shape (height, width, 2). The function should
return an array containing the modified vectors. 

`horizontal_motion_example.py` contains the equivalent python script of the js script presented in the
[ffglitch tutorial](https://ffglitch.org/2020/07/mv.html).

`average_motion_example.py` is the equivalent of this [ffglitch average motion tutorial](https://ffglitch.org/2020/07/mv_avg.html)
using numpy. Neat!

### Warning

Only `numpy` is installed in vector_motion.exe. 
If you want to use your own script and use third party libraries other than numpy, 
you need to use vector_motion.py directly on the command line, or create a new exe file with `pyinstaller`.

## Style transfer

The following settings are available in StyleTransfer.

| Command | Description |
| ------- | ----------- |
| `Vector` | File containing vector data to transfer |
| `Extract` | Video to extract motion vector data from |
| `Transfer` | Video to transfer motion vector data to |
| `Output` | Output file either for the final video, or for the vector data |

I call style transfer combining the motion vectors of two videos (by simply adding them together). For example,
applying the vector motion data of a person talking to a video of clouds can make it look as though the clouds
are talking. 

This script can also extract motion vector data from a video and write it to a file, or read motion data from file and
apply it to a video.

### Examples

| Extract style from | Transfer style to | Result |
|:------------------:|:-----------------:|:------:|
| ![clouds](https://user-images.githubusercontent.com/31802439/112489124-70a21c00-8d7e-11eb-8640-6817a46602ca.gif) | ![trees](https://user-images.githubusercontent.com/31802439/112489146-74ce3980-8d7e-11eb-9091-999fbb98552c.gif) | ![ct](https://user-images.githubusercontent.com/31802439/112489221-86afdc80-8d7e-11eb-9a51-14d91ec7cdfa.gif) |

| Command | Description |
| ------- | ----------- |
| `Extract` | clouds.mp4 |
| `Transfer` | trees.mp4 |
| `Output` | output.mp4 |

    $ python style_transfer.exe -e clouds.mp4 -t trees.mp4 output.mp4

extracts vector data from `clouds.mp4`, transfers it to `trees.mp4` and outputs the video to `output.mp4`.

    $ python style_transfer.exe -e clouds.mp4 vectors.json

extracts the vector data from `clouds.mp4` and outputs it to `vectors.json`.


    $ python style_transfer.exe -v vectors.json -t trees.mp4 output.mp4

loads vector data from `vectors.json`, transfers it to `trees.mp4` and outputs the video to `output.mp4`.
