import sys
import codecs
import re
import lxml.html
from fuzzywuzzy import fuzz

filename = sys.argv[1]

try:
    with codecs.open(filename, "r", "utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    sys.exit()

text_path = re.sub(r"(.*\/)[^\/]*$", r"\g<1>", filename)

hfilename = re.sub(r".*\/([^\/]*)$", r"\g<1>", filename)
hfilename = re.sub(r"\.txt$", r".cms", hfilename)

with codecs.open(hfilename, "rb", "utf-8") as g:
    html_file = g.read()

doc = lxml.html.document_fromstring(html_file)
title = doc.xpath("//h1[@class='heading1']/text()")
time = doc.xpath("string(//span[@class='time_cptn'])")

if not title:
    title = doc.xpath("//title/text()")

"""
soup = BeautifulSoup(html, 'html.parser')
title = soup.find("h1", class_="heading1")
time = soup.find("span", class_="time_cptn")

if not title:
    title = soup.find("title")
"""
if title and time:
    title = re.sub(r"\n|\r", r"", str(title[0]))
    time = re.sub(r"\n|\r", r"", str(time))
    time = re.sub(r"\n|\r", r"", str(time))
    time = re.sub(r"\n|\r", r"", str(time))
    time = re.sub(r"\n|\r", r"", str(time))
    if not any(fuzz.ratio(title,line)>70 for line in lines):
        lines.insert(0,time)
        lines.insert(0,title)
else:
    with codecs.open(text_path + "no_title_or_time", "a", "utf-8") as h:
        h.write(re.sub(r".*\/([^\/]*)$", r"\g<1>", filename))

with codecs.open(filename, "w", "utf-8") as f:
    for line in lines:
        if line:
            line = re.sub(r"\n|\r", r"", line)
            f.write(line + "\n")
