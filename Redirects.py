import sys, os, numpy, re, fileinput, gzip, gc, time
from myprint import myprint as p
from unidecode import unidecode

"""
Program to find all Wikipedia redirects.
The program returns a file containing the pageid and the article title of the
redirect pages.
"""

try:
    titlefilename = sys.argv[1]
    outputtitlesfilename = sys.argv[2]
except:
    print "\n[RUN]: \n"\
    "python Redirecting.py \n"\
    "\t [enwiki-latest-redirects.sql.gz]\n"\
    "\t [output-redirect-titles.txt.gz]\n\n"\
    "[FUNC:]\n"\
    "Find all titles that redirecs \n"
    exit(0)

redirects = dict()  #Dictionary for keeping all redirect pages
starttime = time.time()

# Reads the redictfile
p("Reading all redirect titles", "info")
with gzip.open(titlefilename) as titlefile:
    for line in titlefile:
        if line.startswith("INSERT"):
            line.decode('utf-8', 'ignore')
            line_split = line[30:] #.split("VALUES (")[1]
            insertions = line_split.split("),(")
            for insertion in insertions:

                # Code for encoding
                try:
                    insertion = insertion.decode('unicode-escape')
                except SyntaxError:
                    insertion = insertion.decode('ascii')
                except Exception,e:
                    a = 0

                try:
                    insertion = unidecode(insertion)
                except UnicodeEncodeError, e:
                    print str(e)
                    print insertion
                except Exception,e:
                    print str(e)
                    print insertion
                insertion = insertion.lower()

                words = insertion.split(",")
                pageid = words[0]

                # Finding the title of the redirect page
                if len(words) > 5:
                    title_list = words[2:-2]
                    title = ""
                    for word in title_list:
                        title += word
                    title = title[1:-1]
                else:
                    pagetitle = words[2][1:-1]

                # Code for cleaning the title
                cleantitle = pagetitle.replace("_", " ")
                cleantitle = cleantitle.replace("\\'", "'")
                redirects[pageid] = cleantitle

# Writes all redirect titles and their ids to file
p("Writing all redirect titles to file", "info")
with gzip.open(outputtitlesfilename, "wb") as outputtitles:
    for pageid in redirects:
        outputtitles.write("%s,%s\n" %(pageid, redirects[pageid]))
outputtitles.close()
gc.collect()
