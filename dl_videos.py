import subprocess
import csv
import sys

csv_file = sys.args[1]

with open(csv_file) as csvfile:
    vidreader = csv.reader(csvfile)
    for row in vidreader:
        name = row[0]
        vid = row[1]
        subprocess.run(["youtube-dl", vid])

