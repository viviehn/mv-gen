import os
import sys
import math
import subprocess
import shlex

'''
Most of this code was borrowed from 
https://github.com/c0decracker/video-splitter/blob/master/ffmpeg-split.py
'''

def get_video_length(filename):
    cmd_to_run = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "-i", filename]
    print("About to run: "+" ".join(cmd_to_run))
    output = subprocess.check_output((cmd_to_run)).strip()
    video_length = int(float(output))
    print("Video length in seconds: "+str(video_length))

    return video_length

def ceildiv(a, b):
    return int(math.ceil(a / float(b)))

def split_by_seconds(filename, output_dir, split_length, starting_num, vcodec="copy", acodec="copy",
                     extra="", video_length=None, **kwargs):
    #filename = "\"" + filename + "\""
    if split_length and split_length <= 0:
        print("Split length can't be 0")
        raise SystemExit

    if not video_length:
        video_length = get_video_length(filename)
    split_count = ceildiv(video_length, split_length)
    if(split_count == 1):
        print("Video length is less then the target split length.")
        raise SystemExit

    split_cmd = ["ffmpeg", "-i", filename] + shlex.split(extra)
    try:
        filebase = ".".join(filename.split(".")[:-1])
        fileext = filename.split(".")[-1]
    except IndexError as e:
        raise IndexError("No . in filename. Error: " + str(e))
    for n in range(0, split_count-1):
        split_args = []
        if n == 0:
            split_start = 0
            #subprocess.check_output(["mkdir", filebase])
        else:
            split_start = split_length * n

        split_args += ["-ss", str(split_start), "-t", str(split_length),
                       output_dir + "/" + str(starting_num + n) + "." + fileext]
        print("About to run: "+" ".join(split_cmd+split_args))
        subprocess.check_output(split_cmd+split_args)
    return split_count


def split_video(vid_to_split, output_dir, starting_num, split_length):

    working_dir = vid_to_split
    split_count = split_by_seconds(working_dir, output_dir, split_length, starting_num)
    return split_count

