# File for building complete paths for all articles.
import sys, os, numpy, re, fileinput, gzip, gc, time, Queue
from myprint import myprint as p
import idmapper
"""

"""
try:
    categoryinfofilename = sys.argv[1]
    articleinfofilename = sys.argv[2]
    outputfilename = sys.argv[3]
except:
    print "\n[RUN]: \n"\
    "python Article_path_builder.py \n"\
    "\t [category-info.txt]\n"\
    "\t [article-info.txt.gz]\n"\
    "\t [article-output.txt.gz] \n\n"\
    "[FUNC:]\n"\
    "Create the complete paths of the articles. \n"
    exit(0)

startcategory = "Main topic classifications" #"Fundamental Categories"
firstsubcategories = ["agriculture", "architecture", "arts", "behavior", "business", "chronology", "concepts", "creativity", "culture", "diciplines", "economics", "education", "environment", "form", "geography", "government", "health", "history", "humanities", "humans", "industry", "information", "intellectual works", "knowledge", "language", "law", "leisure", "life", "mathematics", "matter", "medicine", "mind", "nature", "people", "politics", "professional studies", "science", "scientific disciplines", "society", "sports", "structure", "systems", "technology", "thought", "tools", "transport", "universe", "world"]
startcategory = startcategory.lower()
parent = ""
graph = dict()    #Dictionary to keep track of the children to each parent cat
subgraph = dict() #Dictionary to keep track of the parents to each subcategory

starttime = time.time()
begintime = starttime
p("Reading all category info", "info")
parent = child = ""
with open(categoryinfofilename) as categorygraph:
    for line in categorygraph:
        line = line.strip()
        if line.startswith("*"): #children
            child = line[2:]
            idmapper.insert_name(child)
            if parent == "":
                continue
            if parent in graph:
             #   if child not in graph[parent]:
                graph[parent].append(child)
            else:
                graph[parent] = [child]
        else:
            line = line.replace("_", " ")
            parent = line
            idmapper.insert_name(parent)

p("Finished reading all info [Time: %s sec]" %(time.time()-starttime), "info")

with open("graph.txt", "w") as outputfile:
    for parent in graph:
        outputfile.write("%s:\n%s\n\n" %(parent, graph[parent]))
outputfile.close()
p("Graph written to file\n", "info")

articlegraph = dict() #Store all the info of the first subcat to each article
p("Reading all the article info", "info")
articlename = categoryname = ""
artcnt = 0
with gzip.open(articleinfofilename) as articleinfo:
    for line in articleinfo:
        line = line.strip()

        if line.startswith("*"):
            # Found category:
            category = line[2:]
            idmapper.insert_name(category)

            if category in articlegraph:
               # if articlename not in articlegraph[category]:
                articlegraph[category].append(articlename)
            else:
                articlegraph[category] = [articlename]
        else:
            articlename = line
            idmapper.insert_name(articlename)


p("Finished reading all article (%d) info [Time: %s sec (%.3f min)]" %(artcnt, time.time()-starttime, (time.time()-starttime)/60), "info")


def is_number (input):
    try:
        int(input)
        return True
    except:
        return False

def contains_number(input):
    split_input = input.split(" ")
    if len(split_input) < 1 :
        return False
    for word in split_input:
        if is_number(word):
            return True
    return False

skipwords = ["century", "by", "stubs", "location", "nationality"]
def remove_category (input):
    if is_number(input):
        return True
    if contains_number(input):
        return True
    if "millennia" == input:
        return True
    if any(word in input for word in skipwords):
        return True
    return False

artpaths = dict()
found = dict()
articlepaths = dict()

def find_path(category):
    global articlegraph
    global graph
    global found
    global artpaths
    global firstsubcategories

    topcategory = category
    categorypaths = dict()
    categorypaths[category] = category
    q = Queue.Queue()

    subcats = graph[category]
    for subcat in subcats: 
        q.put(subcat)
        categorypaths[subcat] = topcategory + "/-/" + subcat
#    q.put(category)
#    first = True
    while q.qsize() > 0:

        category = q.get()
       
        if category in firstsubcategories:
            print "Met firstcategory (%s)" %(category)
            continue

        thispath = categorypaths[category] # Find my path so far.

        # Check if the category leads to an article
        if category in articlegraph:
            articles = articlegraph[category]
            for article in articles:
                if is_number(article):
                    continue

                # Store all paths to article.
                if article not in artpaths:
                    artpaths[article] = dict()
                    artpaths[article][thispath] = 1
                elif thispath not in artpaths[article]:
                    artpaths[article][thispath] = 1
                # Could also count all occurrences that lead to this solution

                articlepath = thispath + "/" + article
                #print_path_loop(articlepath)

        if category in graph:
            subcats = graph[category]
            for subcat in subcats:
                if subcat in categorypaths:
                    a = 0
                else:
                    subcatpath = thispath
                    #if remove_category(subcat) == False:
                    subcatpath = subcatpath + "/" + subcat
                    categorypaths[subcat] = subcatpath
                    q.put(subcat)

    return artpaths

def artpaths_to_file(artpaths):

    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", \
                   "t", "u", "v", "w", "x", "y", "z"]
    files = []
    for letter in letters: 
        files.append(gzip.open(letter + ".txt.gz", "ab"))
   
    files.append(gzip.open("restfile.txt.gz", "ab"))
        
    cnt = 0
    for article in artpaths:
        if ((cnt % 10000) == 0): 
            for myfile in files: 
                myfile.close()
            files = []
            for letter in letters: 
                files.append(gzip.open(letter + ".txt.gz", "ab"))
            files.append(gzip.open("restfile.txt.gz", "ab"))
        cnt += 1
        firstletter = article[0]
        index = ord(firstletter) -97
        try: 
            files[index].write("%s:\n" %(article))
            paths = artpaths[article]
            for path in paths:
                files[index].write("*%s\n" %(path))
        except Exception, e:
            
                files[-1].write("%s:\n" %(article))
                paths = artpaths[article]
                for path in paths:
                    files[-1].write("*%s\n" %(path))
                    
    for myfile in files: 
        myfile.close()

starttime = time.time()
p("Starting to find article paths", "info")
subcategories = graph[startcategory]
firstsubcategories = subcategories
found = dict()

for subcat in subcategories:
    found = dict()
    articlepaths = dict()
    artpaths = dict()
    starttime = time.time()
    p("Finding all article paths from %s\n" %(subcat), "info")
    artpaths = find_path(subcat)
    #break
    p("Writing all paths to file, Time to find all art paths: %.3f min" %((time.time()-starttime)/60), "info")
    artpaths_to_file(artpaths) #("long-output-"+subcat+".txt.gz", artpaths)
    p("Finished writing all paths to file, Time to write all art paths to file: %.3f min (begin time: %.3f)" %((time.time()-starttime)/60, (time.time()-begintime)/60), "info")

print "Total time: %.3f\n" %((time.time()-starttime)/60)
