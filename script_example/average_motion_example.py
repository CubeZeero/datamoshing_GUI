import numpy as np


average_length = 10


def average(frames):
    if not frames:
        return []
    return np.mean(np.array([x for x in frames if x != []]), axis=0).tolist()


def mosh_frames(frames):
    return [average(frames[i + 1 - average_length: i + 1]) for i in range(len(frames))]
