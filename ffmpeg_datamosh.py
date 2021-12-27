#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('input_video', type=str, help='File to be moshed')
parser.add_argument('--start_frame', '-s', default=0, type=int, help='start frame of the mosh')
parser.add_argument('--end_frame', '-e', default=-1, type=int, help='end frame of the mosh')
parser.add_argument('--fps', '-f', default=30, type=int, help='fps to convert initial video to')
parser.add_argument('-o', default='moshed.mp4', type=str, dest='output_video', help='output file for the moshed video')
parser.add_argument('--delta', '-d', default=0, type=int, help='number of delta frames to repeat')
args = parser.parse_args().__dict__

input_video = args['input_video']
start_frame = args['start_frame']
end_frame = args['end_frame']
fps = args['fps']
delta = args['delta']
output_video = args['output_video']

input_avi = 'datamoshing_input.avi'  # must be an AVI so i-frames can be located in binary file
output_avi = 'datamoshing_output.avi'

# convert original file to avi
subprocess.call('ffmpeg -loglevel error -y -i ' + input_video + ' ' +
                ' -crf 0 -pix_fmt yuv420p -bf 0 -b 10000k -r ' + str(fps) + ' ' +
                input_avi, shell=True)

# open up the new files so we can read and write bytes to them
in_file = open(input_avi, 'rb')
out_file = open(output_avi, 'wb')


def cleanup():
    # gets rid of the in-between files so they're not crudding up your system
    in_file.close()
    out_file.close()
    os.remove(input_avi)
    os.remove(output_avi)

    print('video glitch successfully.')
    sys.exit()


# because we used 'rb' above when the file is read the output is in byte format instead of Unicode strings
in_file_bytes = in_file.read()

# 0x30306463 which is ASCII 00dc signals the end of a frame.
frame_start = bytes.fromhex('30306463')

# get all frames of video
frames = in_file_bytes.split(frame_start)

# write header
out_file.write(frames[0])
frames = frames[1:]

# 0x0001B0 signals the beginning of an i-frame, 0x0001B6 signals a p-frame
iframe = bytes.fromhex('0001B0')
pframe = bytes.fromhex('0001B6')


n_video_frames = len([frame for frame in frames if frame[5:8] == iframe or frame[5:8] == pframe])
if end_frame < 0:
    end_frame = n_video_frames


def write_frame(frame):
    out_file.write(frame_start + frame)


def mosh_iframe_removal():
    for index, frame in enumerate(frames):
        if index < start_frame or end_frame < index or frame[5:8] != iframe:
            out_file.write(frame_start + frame)


def mosh_delta_repeat(n_repeat):
    # check we have enough room to repeat
    if n_repeat > end_frame - start_frame:
        print('not enough frames to repeat')
        cleanup()

    repeat_frames = []
    repeat_index = 0
    for index, frame in enumerate(frames):
        # I don't know why this is a thing but it is
        if (frame[5:8] != iframe and frame[5:8] != pframe) or not start_frame <= index < end_frame:
            write_frame(frame)
            continue

        if len(repeat_frames) < n_repeat and frame[5:8] != iframe:
            # get initial frames to write
            repeat_frames.append(frame)
            write_frame(frame)
        elif len(repeat_frames) == n_repeat:
            write_frame(repeat_frames[repeat_index])
            repeat_index = (repeat_index + 1) % n_repeat
        else:
            # this case happens when the starting frame is an iframe
            write_frame(frame)


if delta:
    mosh_delta_repeat(delta)
else:
    mosh_iframe_removal()


# export the video
subprocess.call('ffmpeg -loglevel error -y -i ' + output_avi + ' ' +
                ' -crf 18 -pix_fmt yuv420p -vcodec libx264 -acodec aac -b 10000k -r ' + str(fps) + ' ' +
                output_video, shell=True)

cleanup()
