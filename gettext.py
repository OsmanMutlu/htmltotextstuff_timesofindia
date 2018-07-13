import justext
import re
import sys
import os

filename=sys.argv[1]

#This is the folder containing text files
text_path = "../random_newstext/"

file = open(filename, "r")
html = file.read()
file.close()

ofilename = re.sub(r"\.cms$", r".txt", filename)
ofile = open(text_path + ofilename, "a")

paragraphs = justext.justext(html,justext.get_stoplist("English"))
for paragraph in paragraphs:
  if not paragraph.is_boilerplate:
    ofile.write(paragraph.text + "\n")

ofile.close()
