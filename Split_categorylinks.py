# -*- coding: utf-8 -*-
import sys, os, numpy, re, fileinput, gzip, gc, time, io, json
from myprint import myprint as p
from unidecode import unidecode

"""
Program that split the file "enwiki-latest-categroylinks.sql.gz" into two files: 
- file containing links between categories
- file containing links between categories and articles
It also skips all links to pages that are disambiguation pages or numbers and skips
all links between hidden categories and articles. 
"""

categoryinputfilename = "enwiki-latest-categorylinks.sql.gz"
categoryoutputfilename = "Sub-categories.txt.gz"
pageoutputfilename = "Page-categories.txt.gz"
hiddencategoryinputfilename = "All_hidden_categories.txt.gz"
redirectinputfilename = "output-redirect-titles.txt.gz"

def is_number (input):
    try:
        int(input)
        return True
    except:
        return False

start_time = time.time()
categorycnt = pagecnt = lines = 0

hidden_cat = dict()
artskip = catskip = hiddencnt = 0

p("Reading all hidden categories", "info")
with gzip.open(hiddencategoryinputfilename) as hiddencategories:
    for line in hiddencategories:
        line = line.strip().lower()
        if line in hidden_cat:
            hidden_cat[line]+=1
        else:
            hidden_cat[line]=1
p("All hidden categories read", "info")

redirects = dict()
p("Reading all redirects", "info")
with gzip.open(redirectinputfilename, "rb") as redirectfile:
    for line in redirectfile:     
        line.decode('utf-8', 'ignore')
        line = line.lower()
        split_line = line.split(",")
        pageid = split_line[0]
        pagename = split_line[1]
        #if category not in redirects:
        redirects[pageid] = pagename
p("Finsihed readling all redirects", "info")

disambiguationtitles = dict()
with gzip.open("all-disambiguation-titles.txt.gz", "rb") as disambfile: 
    for line in disambfile: 
        line.decode('utf-8', 'ignore')
        line = line.strip()
        line = line.lower()
        disambiguationtitles[line] = 1


ignorelist = ["wikiproject"] 
remove_links = dict()

hiddencatlinks = dict()
pages = dict()
cats = dict()
allnumbercategories = dict()
disambg = dict()

p("Reading content...", "info")
with gzip.open(categoryinputfilename) as inputfile: 
    for line in inputfile:
        if (line.startswith("INSERT")):
            line = line[35:]
            line = line.lower()

            # Regex for separating entries in the insert statement
            regex = "(\(\d+\,.*?\,('file'|'page'|'subcat')\))"           
            insertions = re.findall(regex, line)
            for insertion in insertions:
                insertion = insertion[0]

                words = insertion.split("','")
                words[0] = words[0][1:]
                words[-1] = words[-1][:-1]

                insertion_id = words[0].split(",")[0]
                from_link = words[0].split(insertion_id)[1][2:]
                to_link = words[1]
                        
                #if from_link in ignorelist or to_link in ignorelist:
                if any(item in from_link for item in ignorelist) or \
                        any(item in to_link for item in ignorelist): 
                    continue

                if insertion_id in redirects:
                    before = to_link
                    to_link = redirects[insertion_id]

                # Found a link between categories 
                if words[-1] == "subcat'": 
                    sortkey = words[4][:-1]
                    
                    # Cleaning the category names
                    parent_category = from_link.replace("_", " ")               
                    to_category = to_link.replace("_", " ")

                    # Storing the category link
                    if "\\n" in to_category:
                        split_cat = to_category.split("\\n")

                        if parent_category in cats: 
                            cats[parent_category].append(split_cat[1])
                        else: 
                            cats[parent_category] = [split_cat[1]]
                    else:
                        if parent_category in cats: 
                            cats[parent_category].append(to_category)
                        else: 
                            cats[parent_category] = [to_category]

                # Found a link between category and article
                elif words[-1] == "page'": 

                    # Cleaing the category and article name
                    category_name = from_link.replace("_", " ")
                    page_name = to_link.replace("_", " ")
                    
                    # If the category is a hidden category; skip
                    if category_name in hidden_cat:
                        continue

                    # If the page is a disambiguation page; skip 
                    if page_name in disambiguationtitles: 
                        continue

                    # If the page or the category is a number; skip
                    if is_number(category_name) or is_number(page_name):
                        if is_number(page_name): 
                            allnumbercategories[page_name] = 1
                        continue

                    # Storing the link between the category and the page 
                    if "\\n" in page_name:
                        page_split = page_name.split("\\n")
                        if page_split[0] == page_split[1]:
                            page_name = page_split[0]
                        elif page_split[0] == "":
                            page_name = page_split[1]
                        elif page_split[1] == "":
                            page_name = page_split[0]
                        elif "," in page_name:
                            page_name = page_split[1]
                        elif len(page_split[0]) > len(page_split[1]):
                            page_name = page_split[0]
                        else:
                            page_name = page_split[1]
                    if category_name in pages: 
                        pages[category_name].append(page_name)
                    else: 
                        pages[category_name] = [page_name]
                         
p("Diambiguation links found: %d" %(diambg), "info")

# Wrting all links between categories to file
p("Writing category links to file", "info")
with gzip.open(categoryoutputfilename, "wb") as categoryoutput:
    for category in cats: 
        outcategory = category
        try:
            outcategory = outcategory.decode('unicode-escape')
        except SyntaxError: 
            outcategory = outcategory.decode('ascii')
        except Exception,e:
            a = 0    
        try: 
            outcategory = unidecode(outcategory)
        except: 
            a = 0      
        outcategory = outcategory.lower()
        for subcat in cats[category]: 
            outsubcat = subcat
            try:
                outsubcat = outsubcat.decode('unicode-escape')
            except SyntaxError: 
                outsubcat = outsubcat.decode('ascii')       
            try: 
                outsubcat = unidecode(outsubcat)
            except: 
                a = 0
            outsubcat = outsubcat.lower()
            line = outcategory + "\t" + outsubcat + "\n" 
            categoryoutput.write(line)

categoryoutput.close()

# Writing all links between categories and articles to file
p("Writing page links to file", "info")
with gzip.open(pageoutputfilename, "wb") as pageoutput:
    for category in pages : 
        outcategory = category
        try:
            outcategory = outcategory.decode('unicode-escape')
        except SyntaxError: 
            outcategory = outcategory.decode('ascii')       
        try: 
            outcategory = unidecode(outcategory)
        except: 
            a = 0
        outcategory = outcategory.lower()
        for page in pages[category]: 
            outpage = page
            try:
                outpage = outpage.decode('unicode-escape')
            except SyntaxError: 
                outpage = outpage.decode('ascii')       
            except: 
                a = 0
            try: 
                outpage = unidecode(outpage)
            except: 
                a = 0
            outpage = outpage.lower()         
            line = outcategory + "\t" + outpage + "\n"
            pageoutput.write(line)

mytime = time.time() - start_time
p("--- %s seconds (%s min, %s min) ---" %(mytime, mytime/60, mytime%60), "info")
gc.collect()
