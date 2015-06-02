import sys, os, numpy, re, fileinput, gzip, gc, time
from myprint import myprint as p

"""
Program for checking if all hidden categories are removed from the category graph.
The program prints and error if a hidden category is found in the category graph.
"""

try:
    categoryinputfilename = sys.argv[1]
    hiddencategoryinputfilename = sys.argv[2]
except:
    print "\n[RUN]: \n"\
    "python Is_hidden_there.py \n"\
    "\t [Subcat-links.txt.gz]\n"\
    "\t [All_hidden_categories.txt.gz]\n"
    exit(0)

hidden_cat = dict()         #Dictionary to check all hidden category names
hiddencnt = 0               #Counter to see how many hidden categories are read
hiddencat_found = False     #Boolean to determine if hidden cateogry is found within graph

# Reads all hidden categories from the file containing the names of all hidden categories
p("Reading all hidden categories", "info")
with gzip.open(hiddencategoryinputfilename) as hiddencategories:
    for line in hiddencategories:
        line = line.strip().lower()
        if line in hidden_cat:
            hidden_cat[line]+=1
        else:
            hiddencnt += 1
            hidden_cat[line]=1
p("All hidden categories read", "info")

# Reads the category graph
p("Read all category links", "info")

with gzip.open(categoryinputfilename, "rb") as inputfile:
    for line in inputfile:
        line = line.strip()
        if line.startswith("*"):
            line = line[2:]
        else:
            line = line[-1]
        if line in hidden_cat:
            # If hidden category is found.
            hiddencat_found = True
inputfile.close()

if hiddencat_found:
    print "ERROR: Found hidden category within the category graph"
else:
    print "No hidden categories found within the category graph"
