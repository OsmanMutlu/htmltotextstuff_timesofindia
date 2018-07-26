import sys
import codecs
import re
import shutil
from glob import glob
import pandas as pd
from dask import dataframe as dd
from dask.multiprocessing import get
import lxml.html
from fuzzywuzzy import fuzz

html_path = sys.argv[1]

files = glob("http*")

all_df = pd.DataFrame(files, columns=["filename"])

all_df["asd"] = ""

#These are the starting lines of the comment section
stoplist = ["RELATED", "From around the web", "More from The Times of India", "Recommended By Colombia",
            "more from times of india Cities","You might also", "You might also like", "more from times of india",
            "All Comments ()+^ Back to Top","more from times of india News","more from times of india TV",
            "more from times of india Sports","more from times of india Entertainment","more from times of india Life & Style",
            "more from times of india Business"]

stoplist2 = ["FOLLOW US","FOLLOW PHOTOS","FOLLOW LIFE & STYLE"]

def clean(row):

    print(row.filename)

    try:
        with codecs.open(row.filename, "r", "utf-8") as f:
            lines = f.readlines()
    except (IOError,FileNotFoundError):
        with codecs.open("empty_files","a","utf-8") as g:
            g.write(row.filename + "\n")
        return row

#Deletesamesubstr
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
        with codecs.open("empty_files","a","utf-8") as g:
            g.write(row.filename + "\n")
        return row

    j = 0
    while j <= len(lines)-1:
        if lines[j]:
            lines[j] = re.sub(r"<[^>]*>", r"", lines[j])
            lines[j] = re.sub(r"\n|\r", r"", lines[j])
            j = j + 1
        else:
            del lines[j]

#Deletecertainstr
    for i in range(0,len(lines)):
        firstline = lines[i]
        firstline = re.sub(r"\n|\r", r"", firstline)
        if any(firstline == word for word in stoplist):
#We delete the same line because when we delete the item, item index shifts 1 number
            for j in range(i, len(lines)):
                del lines[i]
            break

    if not lines or all(len(line)==0 for line in lines):
        with codecs.open("empty_files","a","utf-8") as g:
            g.write(row.filename + "\n")
        return row

#Deletecertainstr2
    n = 0
    while n < len(lines)-1:
        if not lines[n]:
            n = n + 1
            continue
        line = lines[n]
        line = re.sub(r"\n|\r", r"", line)
        if any(line == word for word in stoplist2):
            del lines[n]
            continue
        n = n + 1

    if not lines or all(len(line)==0 for line in lines):
        with codecs.open("empty_files","a","utf-8") as g:
            g.write(row.filename + "\n")
        return row

#Addnewstime
    hfilename = re.sub(r"\.txt$", r".cms", row.filename)

    with codecs.open(html_path + hfilename, "rb", "utf-8") as g:
        html_file = g.read()

    doc = lxml.html.document_fromstring(html_file)
    title = doc.xpath("//h1[@class='heading1']/text()")
    time = doc.xpath("string(//span[@class='time_cptn'])")

    if not title:
        title = doc.xpath("//title/text()")

    if title and time:
        title = re.sub(r"\n|\r", r"", str(title[0]))
        time = re.sub(r"\n|\r", r"", str(time))
        if not any(fuzz.ratio(title,line)>70 for line in lines):
            lines.insert(0,time)
            lines.insert(0,title)
    else:
        with codecs.open("no_title_or_time", "a", "utf-8") as h:
            h.write(re.sub(r".*\/([^\/]*)$", r"\g<1>", row.filename))

#Deletesamesubstr
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
        with codecs.open("empty_files","a","utf-8") as g:
            g.write(row.filename + "\n")
        return row

#Addnewslink
    link = re.sub(r"___", r"://", row.filename)
#    link = re.sub(r"__", r"://", row.filename)
    link = re.sub(r"_", r"/", link)
    link = re.sub(r"\.txt$", r".cms", link)
    lines.append("url : " + link)

    with codecs.open(row.filename, "w", "utf-8") as f:
        for line in lines:
            if line:
                line = re.sub(r"\n|\r", r"", line)
                f.write(line + "\n")

    return row

all_df = dd.from_pandas(all_df,npartitions=3).map_partitions(lambda df : df.apply(clean, axis=1),meta=all_df).compute(get=get)
