import sys, os, numpy, re, fileinput, gzip, gc, time
from myprint import myprint as p
from unidecode import unidecode

"""
Program to fint the name of all hidden categories within the category structure.
The program find the ids from enwiki-latest-page_props, and the corresponding
category names from enwiki-latest-page.
"""

try:
    pagepropsinputfilename = sys.argv[1]
    pageinputfilename = sys.argv[2]
    hiddencategoryoutputfilename = sys.argv[3]
except:
    print "\n[RUN]: \n"\
    "python Hidden_categories.py \n"\
    "\t [enwiki-latest-page_props.sql.gz]\n"\
    "\t [enwiki-latest-page.sql.gz\n"\
    "\t [All_hidden_categories.txt.gz]\n\n"\
    "[FUNC:] Find all hidden categories in the categorylinks file and then in the page_props file and combine all of these to one big file. \n"
    exit(0)


hiddencat_id = dict()   #Dictionary to keep track of the ids of all hidden categories
hidden_cat = dict()     #Dictionary to keep track of the name of all hidden categories
hiddencnt = 0
start_time = time.time()

# Looping through page props to find the ids of all hidden categories
p("Finding all hidden category ids from page props...", "info")
with gzip.open(pagepropsinputfilename) as inputfile:
    for line in inputfile:
        if (line.startswith("INSERT")):
            line = line.split("VALUES (")[1]
            line.decode('utf-8', 'ignore')
            insertions = line.split("),(")
            for insertion in insertions:
                insertion = insertion.lower()
                words = insertion.split(",")
                if "hiddencat" in words[1].lower():
                    # Hidden category is found, id i added
                    hiddencat_id[words[0]] = 1
                    hiddencnt += 1  # Counter to keep track of number of hidden categories
mytime = time.time() - start_time
p("Found %d hidden category ids (%s min, %s min) ---" %(hiddencnt,  mytime/60, mytime%60), "info")

categorycnt = 0    # Counter to keep track of number of hidden categories

# Looping through pages and find the name of all the hidden categories
p("Finding the name of the hidden category ids", "info")
with gzip.open(pageinputfilename) as inputfile:
    for line in inputfile:
        if (line.startswith("INSERT")):
            line = line.split("VALUES (")[1]
            line.decode('utf-8', 'ignore')
            insertions = line.split("),(")
            for insertion in insertions:
                insertion = insertion.lower()

                words = insertion.split(",")
                # Only interested in categories, namespace 14 is category
                if words[1] == "14":
                    if words[0] in hiddencat_id:
                        words = insertion.split(",")
                        # Combine the title of the category
                        if len(words) > 12:
                            title_list = words[2:-10]
                            title = ""
                            for word in title_list:
                                title += word
                            title = title[1:-1]
                        else:
                            title = words[2][1:-1]
                        title = title.replace("_", " ") # Clean the title
                        # Add the title
                        if title not in hidden_cat:
                            categorycnt += 1
                            hidden_cat[title] = 1
mytime = time.time() - start_time
p("Total: Found %d hidden categories  (%s min, %s min) ---" %(len(hidden_cat), mytime/60, mytime%60), "info")

# Write the results to file
p("Writing all hidden categories to file", "info")
with gzip.open(hiddencategoryoutputfilename, "wb") as outputcategory:
    for category in hidden_cat:
        outputcategory.write("%s\n" %(category))
outputcategory.close()
p("%d hidden category names written to %s" %(categorycnt,hiddencategoryoutputfilename), "info")
