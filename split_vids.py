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

    output = subprocess.check_output(("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename)).strip()
    video_length = int(float(output))
    print "Video length in seconds: "+str(video_length)

    return video_length

def ceildiv(a, b):
    return int(math.ceil(a / float(b)))

def split_by_seconds(filename, split_length, vcodec="copy", acodec="copy",
                     extra="", video_length=None, **kwargs):
    if split_length and split_length <= 0:
        print "Split length can't be 0"
        raise SystemExit

    if not video_length:
        video_length = get_video_length(filename)
    split_count = ceildiv(video_length, split_length)
    if(split_count == 1):
        print "Video length is less then the target split length."
        raise SystemExit

    split_cmd = ["ffmpeg", "-i", filename, "-vcodec", vcodec, "-acodec", acodec] + shlex.split(extra)
    try:
        filebase = ".".join(filename.split(".")[:-1])
        fileext = filename.split(".")[-1]
    except IndexError as e:
        raise IndexError("No . in filename. Error: " + str(e))
    for n in range(0, split_count):
        split_args = []
        if n == 0:
            split_start = 0
            subprocess.check_output(["mkdir", filebase])
        else:
            split_start = split_length * n

        split_args += ["-ss", str(split_start), "-t", str(split_length),
                       filebase + "/" + str(n+1) + "." + fileext]
        print "About to run: "+" ".join(split_cmd+split_args)
        subprocess.check_output(split_cmd+split_args)

working_dir = os.getcwd() + "/" + sys.argv[1]
split_length = 10  # seconds

files = [f for f in os.listdir(working_dir) if os.path.isfile(working_dir+f)]
for f in files:
    split_by_seconds(working_dir + f, split_length)


