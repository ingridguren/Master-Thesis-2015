from __future__ import division

import sys, os, numpy, re, fileinput, gzip, gc, time, Queue, collections
from operator import itemgetter
from myprint import myprint as p

class Path(object): 
    def __init__(self, score, path): 
        self.score = score
        self.path = path
        return 
    def __cmp__(self, other): 
        return cmp(other.score, self.score)
        
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", \
               "t", "u", "v", "w", "x", "y", "z", "restfile"]

gradesfilename = "category-grade.txt.gz"
idfilename = "id-mapper.txt.gz"

p("Reading all grades", "info")
allgrades = dict()
grades = dict()
with gzip.open(gradesfilename, "rb") as gradefile: 
#with open(gradesfilename, "r") as gradefile: 
    for line in gradefile: 
        line = line.strip()
        splittet = line.split("\t")
        category = splittet[0]
        #print line
        grade = float(splittet[1])
        grades[category] = grade

id_to_name = dict()
p("Reading all ids for all categories", "info")
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
        


for letter in letters: 
    inputfilename = letter + "id.txt.gz"
    outputfilename = "best-" + letter + ".txt.gz"
    idoutputfilename = "best-" + letter + "-id.txt.gz"
    
    artpaths = dict()
    p("Reading all categories for letter %s" %(letter), "info")
    with gzip.open(inputfilename, "rb") as inputfile: 
        for line in inputfile: 
            line = line.strip()

            if line.startswith("*"): 
                # path found
                path = line[1:]
                if article in artpaths: 
                    artpaths[article][path] = 1
                else: 
                    artpaths[article] = dict()
                    artpaths[article][path] = 1
            else: 
                article = line[:-1]

    p("Finished reading the whole file", "info")
    p("Grading all paths", "info")
    with gzip.open(outputfilename, "wb") as outputfile: 
        with gzip.open(idoutputfilename, "wb") as idoutputfile: 
            for article in artpaths: 
                que = Queue.PriorityQueue()
                worse = 0
                for artpath in artpaths[article]: 
                    pathscore = 0
                    cats_in_path = artpath.split("/")
                    pathcatcnt = 0
                    for cat in cats_in_path: 
                        pathcatcnt+=1
                        if cat in grades: 
                            pathscore += grades[cat]
                        else: 
                            print "%s: %s\n" %(pathscore, artpath)
                    pathscore = pathscore/pathcatcnt
                    if pathscore in allgrades: 
                        allgrades[pathscore]+=1
                    else: 
                        allgrades[pathscore] = 1
                    if que.qsize() < 3: 
                        que.put(Path(pathscore, artpath))
                        if worse < pathscore: 
                            worse = pathscore
                    elif pathscore < worse: 
                        removed = que.get()
                        que.put(Path(pathscore, artpath))
                        notremoved = que.get()
                        worse = notremoved.score
                        que.put(notremoved)
                
                outputfile.write("%s:\n" %(id_to_name[article]))
                idoutputfile.write("%s:\n" %(article))
                mypaths = []
                while(que.empty() == False): 
                    mypaths.insert(0, que.get())
                for goodpath in mypaths: 
                    idoutputfile.write("*%s (%s)\n" %(goodpath.path, goodpath.score))
                    outputfile.write("* %s\t" %(goodpath.score))
                    for art in goodpath.path.split("/"):
                        outputfile.write("%s/" %(id_to_name[art]))
                    outputfile.write("\n")
        outputfile.close()
gc.collect()
