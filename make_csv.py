import csv
import os
import sys

working_dir = os.getcwd() + '/' + sys.argv[1]

files = [f for f in os.listdir(working_dir) if os.path.isfile(working_dir + f)]
for f in files:
    print(f)

with open(working_dir +'videos_list.csv', mode='w') as videos:
    video_writer = csv.writer(videos)
    for f in files:
        abs_path = working_dir + f
        video_writer.writerow([abs_path, "14"])

