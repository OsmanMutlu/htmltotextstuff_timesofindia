import justext
import re
import sys
import os
import multiprocessing
from glob import glob
import codecs

text_path = sys.argv[1]

#with codecs.open("../didntdo", "r", "utf-8") as h:
#    files = h.read().splitlines()

files = glob("http*")

#print(files)

stoplist = justext.get_stoplist("English")

def asd(filename):

    with open(filename, "rb") as g:
        html = g.read()

    ofilename = re.sub(r"\.cms$", r".txt", filename)

    with codecs.open(text_path + ofilename, "a", "utf-8") as f:
        paragraphs = justext.justext(html,stoplist)
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                f.write(paragraph.text + "\n")

    return filename

p = multiprocessing.Pool(10)
values = p.map(func=asd,iterable=files)
p.close()
