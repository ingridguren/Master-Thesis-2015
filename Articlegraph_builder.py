# -*- coding: utf-8 -*-
import sys, os, numpy, re, fileinput, gzip, gc, time
from myprint import myprint as p

"""
Program that creates the article graph.
Output is a file containing the categories and which articles they contain
"""

try:
    articleinputfilename = sys.argv[1]
    articleoutputfilename = sys.argv[2]
except:
    print "\n\n[RUN]: \n"\
        "python Articlegraph_builder.py \n"\
        "\t [Page-categories.txt.gz]\n"\
        "\t [article-info.txt.gz]\n\n"\
    "[FUNCTION]: \n"\
    "Store all articles with their immidiate subcategories\n"
    exit(0)

reload(sys)
sys.setdefaultencoding('utf-8')


articles = dict()       #Dictionary to keep track of all categories and their articles
artcnt = teller = articlecnt = 0
starttime = time.time()

# Reads the file file containg links between categories and articles
p("Reading all article content...", "info")
with gzip.open(articleinputfilename) as articleinfo:
    for line in articleinfo:
        line = line.strip()
        lines = line.split("\t")
        if len(lines) < 2:
            continue
        category = lines[0].lower()
        page = lines[1].lower()
        if "" == page or " " == page:
            continue

        if page in articles:
            # page is already in the dictionary
            if category not in articles[page]:
                # Add the category if not present
                articles[page][category] = 1
        else:
            # page and category are not in the dictionary
            articles[page] = dict()
            if category not in articles[page]:
                articles[page][category] = 1
p("Finished reading all article info [Time: %s sec (%.3f min)]" %(time.time()-starttime, (time.time()-starttime)/60), "info")

# Write the article graph to file
p("Writing article info to file...", "info")
with gzip.open(articleoutputfilename, 'wb') as articleoutput:
    for articletitle in articles:
        artcnt += 1
        articleoutput.write("%s\n" %(articletitle))
        for category in articles[articletitle]:
            try:
                articleoutput.write(unicode("* %s \n" %(category)).encode('utf-8'))
            except:
                print "Could not write to file\n"
                print category
articleoutput.close()

print "%d articles with info written to %s" %(artcnt, articleoutputfilename)
gc.collect()
