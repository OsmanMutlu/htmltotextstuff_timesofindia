import sys
import codecs
import re

filename = sys.argv[1]
#These are the starting lines of the comment section
stoplist = ["FOLLOW US","FOLLOW PHOTOS","FOLLOW LIFE & STYLE"]

with codecs.open(filename, "r", "utf-8") as f:
    lines = f.readlines()

n = 0
while n < len(lines)-1:
    if not lines[n]:
        n = n + 1
        continue
    line = lines[n]
    line = re.sub(r"\n|\r", r"", line)
    if any(line == word for word in stoplist):
        del lines[n]
        continue
    n = n + 1

if not lines:
    print("FILE IS EMPTY!!! : " + filename)

with codecs.open(filename, "w", "utf-8") as f:
    for line in lines:
        if line:
            line = re.sub(r"\n|\r", r"", line)
            f.write(line + "\n")
