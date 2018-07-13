import justext
import re
import sys
import os
from glob import glob
import codecs
#import pandas as pd
#from dask import dataframe as dd
#from dask.multiprocessing import get
import multiprocessing

text_path = sys.argv[1]

files = glob("http*")

#all_df = pd.DataFrame(files, columns=["filename"])

#all_df["asd"] = ""

def clean(filename):

    with open(filename, "rb") as g:
        html = g.read()

    ofilename = re.sub(r"\.cms$", r".txt", filename)

    paragraphs = justext.justext(html,justext.get_stoplist("English"))

    with codecs.open(text_path + ofilename, "w", "utf-8") as f:
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                f.write(paragraph.text + "\n")

    return filename

#all_df = dd.from_pandas(all_df,npartitions=12).map_partitions(lambda df : df.apply(clean, axis=1),meta=all_df).compute(get=get)

p = multiprocessing.Pool(12)
asd = p.map(func=clean,iterable=files)
p.close()
