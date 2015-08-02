import sys, os, numpy, re, fileinput, gzip, gc, time, Queue, collections, json, io, yaml
from operator import itemgetter
from myprint import myprint as p

"""
Program for mapping all keywords to IAB categories. 
"""

inputfilename = "articlemapping-all.txt.gz"
outputcategoriesfilename = "Outputcategories"

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "restfile"]

outputcategories = dict()

tiertwo = ""
tierone = ""
p("Reading output categories", "info")
with open(outputcategoriesfilename, "r") as outputcatfile: 
    for line in outputcatfile: 
        line = line.strip()
        if line.startswith("*"): 
            tierone = line[1:]
            tierone = line.lower()
        else: 
            tiertwo = line
            tiertwo = line.lower()
            outputcategories[tiertwo] = tierone


idfilename = "id-mapper.txt.gz"
id_to_name = dict()
name_to_id = dict()
p("Reading id-mapper", "info")
with gzip.open(idfilename, "rb") as idfile: 
    for line in idfile: 
        line = line.strip()
        
        regex = "(\d+)\,\s+(.*)"
        identry = re.findall(regex, line)
            
        identry = identry[0]
        if len(identry) < 2: 
            continue
        myid = identry[0]
        myentry = identry[1]
        
        id_to_name[myid] = myentry
        name_to_id[myentry] = myid
        
        

regexliste = dict()

thirdtier = []
tierone = ""
tiertwo = ""
firsttime = True
maptotier = dict()
with open("Outputcategories-2", "r") as outputcatfile: 
#with open("Mapping_booksandliterature", "r") as outputcatfile: 
    for line in outputcatfile: 
        if not line.strip(): 
            continue
        line = line.strip()
        line = line.lower()
        
        if line.startswith("-"): # Found third tier
            
            if "\t" in line: 
                path = line.split("\t")[0][1:]
                notpath = line.split("\t")[1]
            else: 
                path = line[1:]
            
            thirdtier.append(path)
            tiername = tierone + "/" + tiertwo
            maptotier[path] = tiername
        elif line.startswith("#"): 
            tierone = line[1:]
        else: 
            if firsttime == True:
                firsttime = False
                tiertwo = line
                continue
            regexliste[tiertwo] = thirdtier
            tiertwo = line
            thirdtier = []


def writetofile(letter):
    global dictionary
    with io.open("igg-mapping-" + letter + ".txt", 'w', encoding='utf8') as json_file:
        data = json.dumps(dictionary, ensure_ascii=False, encoding='utf8')
        json_file.write(unicode(data))
    json_file.close()

articlesfound = dict()

p("Matching..", "info")
dictionary = dict()
matchedarticles = dict()
starttime = time.time()
allarticles = 0
articlespercategory = dict()
notmatchedarticles = dict()

matchedpaths = dict()
notmatched = True
for letter in letters: 
    p("Mapper for %s" %(letter), "info")
    inputfilename = "best-" + letter + ".txt.gz"
    outputcatfound = True
    printarticle = ""
    with gzip.open(inputfilename, "rb") as inputfile: 
        for line in inputfile:
            line = line.strip()
            if line.startswith("*"):
             
                splittet = line.split("\t")
                score = splittet[0][2:]
                path = splittet[1]
                for liste in regexliste: 
   
                    for regex in regexliste[liste]: 
                
                        if regex in path: 
                            notmatched = False                            
                            tier = maptotier[regex]
                            path_end = path.split(regex)[1]
                            cats_at_end = len(path_end.split("/"))
                            if cats_at_end > 5: 
                                continue

                            if article in matchedarticles: 
                                if tier not in matchedarticles[article]: 
                                    matchedarticles[article].append(tier)
                            else: 
                                matchedarticles[article] = [tier]

                            # Storing all paths to see if they look correct
                            if liste in articlespercategory: 
                                articlespercategory[liste].append(article)
                            else: 
                                articlespercategory[liste] = [article]
                          
                            if liste in articlesfound: 
                                articlesfound[liste]+= 1
                            else: 
                                articlesfound[liste] = 1

                            if regex in matchedpaths: 
                                matchedpaths.append(path)
                            else: 
                                matchedpaths = [path]
                if notmatched == True: 
                    if article in notmatchedarticles: 
                        notmatchedarticles[article].append(path)
                    else: 
                        notmatchedarticles[article] = [path]
            # Found article name 
            else:
                article = line[:-1]
                allarticles+= 1
                notmatched = True

dictionary["igg-iabtaxonomy4"] = matchedarticles
writetofile("all")

p("Time: %.3f min" %((time.time()-starttime)/60), "info")

p("Total number of articles found: %d/%d" %(len(matchedarticles), allarticles), "info")

p("Writing all results to file", "info")
for category in articlespercategory: 
    categorytitle = category
    if "/" in category: 
        splittet_category = category.split("/")
        categorytitle = splittet_category[0] + splittet_category[1]
    with gzip.open("mapping-" + categorytitle + ".txt.gz", "wb") as catfile: 
        catfile.write("%s\n" %(category))
        for path in articlespercategory[category]:
            catfile.write("%s\n" %(path))
    catfile.close()
