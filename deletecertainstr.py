import sys
import codecs
import re
import shutil

filename = sys.argv[1]

#This is the folder containing texts
text_path = re.sub(r"(.*\/)[^\/]*$", r"\g<1>", filename)

#These are the starting lines of the comment section
stoplist = ["RELATED", "From around the web", "More from The Times of India", "Recommended By Colombia",
            "more from times of india Cities","You might also", "You might also like", "more from times of india", "All Comments ()+^ Back to Top"]

try:
    with codecs.open(filename, "r", "utf-8") as f:
        lines = f.readlines()
except (IOError,FileNotFoundError):
    print("FILE IS EMPTY : " + filename)
    sys.exit(1)

for i in range(0,len(lines)):
    firstline = lines[i]
    firstline = re.sub(r"\n|\r", r"", firstline)
    if any(firstline == word for word in stoplist):
#We delete the same line because when we delete the item, item index shifts 1 number
        for j in range(i, len(lines)):
            del lines[i]
        break

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
                line = re.sub(r"\n|\r", r"", line)
                f.write(line + "\n")
