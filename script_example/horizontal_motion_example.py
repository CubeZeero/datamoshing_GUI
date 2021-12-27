def mosh_frames(frames):
    for frame in frames:
        if not frame:
            continue

        for row in frame:
            for col in row:
                # col contains the horizontal and vertical components of the vector
                col[0] = 0

    return frames
