import sys
import codecs
import re
import shutil

filename = sys.argv[1]

#This is the folder containing texts
text_path = re.sub(r"(.*\/)[^\/]*$", r"\g<1>", filename)

try:
    with codecs.open(filename, "r", "utf-8") as f:
        lines = f.readlines()
except (IOError,FileNotFoundError):
    print("FILE IS EMPTY!!! : " + filename)
    sys.exit(1)

#This is specific to timesofindia data that comes from justext

i = 0
while i<=len(lines)-1:
    isDeleted = False
    firstline = lines[i]
    firstline = re.sub(r"\s", r"", firstline)
    firstline = re.sub(r"\W", r"", firstline)
    firstline = re.sub(r"<[^>]*>", r"", firstline)
    for j in range(i+1,len(lines)):
        secondline = lines[j]
        secondline = re.sub(r"\s", r"", secondline)
        secondline = re.sub(r"\W", r"", secondline)
        if firstline.lower() in secondline.lower() and len(firstline)>22:
            del lines[i]
            isDeleted = True
            break
    if not isDeleted:
        i = i + 1

if not lines or all(len(line)==0 for line in lines):
    ofilename = re.sub(r".*\/([^\/]*)$", r"\g<1>", filename)
    print("FILE IS EMPTY!!! : " + ofilename)
    with open(text_path + "empty_files","a") as g:
        g.write(ofilename + "\n")
    shutil.move(filename, text_path + "empties/" + ofilename)

else:
    with codecs.open(filename, "w", "utf-8") as f:
        for line in lines:
            if line:
                line = re.sub(r"<[^>]*>", r"", line)
                line = re.sub(r"\n|\r", r"", line)
                f.write(line + "\n")
