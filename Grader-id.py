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

#letters = ["restfile"]
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
        #name_to_id[myentry] = myid


noofpathsperarticle = dict()
for letter in letters: 
    inputfilename = letter + "id.txt.gz"
    #outputfilename = "best-" + letter + ".txt.gz"
    idoutputfilename = "best-" + letter + "-id.txt.gz"
    articles_not_graded = dict()
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
    with gzip.open("articlesnotgraded" + letter + ".txt.gz", "wb") as notgradedfile: 
        with gzip.open(idoutputfilename, "wb") as idoutputfile: 
            for article in artpaths: 
                que = Queue.PriorityQueue()
                worse = 0
                minpathscore = 100000
                for artpath in artpaths[article]: 
                    pathscore = 0
                    cats_in_path = artpath.split("/")
                    for cat in cats_in_path: 
                        if cat in grades: 
                            pathscore += grades[cat]
                        else: 
                            print "%s: %s\n" %(pathscore, artpath)
#                if pathscore in allgrades: 
#                    allgrades[pathscore]+=1
#                else: 
#                    allgrades[pathscore] = 1
                    
                #if pathscore < 32.701703: 
                    if pathscore < minpathscore: 
                        minpathscore = pathscore
                    if pathscore < 64.026493: 
                   #if pathscore < 999.983648: 
                        que.put(Path(pathscore, artpath))
                        if worse < pathscore: 
                            worse = pathscore
                        elif pathscore < worse: 
                            removed = que.get()
                            que.put(Path(pathscore, artpath))
                            notremoved = que.get()
                            worse = notremoved.score
                            que.put(notremoved)
                
                #idoutputfile.write("%s:\n" %(article))
                mypaths = []
                while(que.empty() == False): 
                    mypaths.insert(0, que.get())
                if len(mypaths) == 0:
                    articles_not_graded[article] = minpathscore
                    #notgradedfile.write("%s (%d)\n" %(article, minpathscore))
                noofpaths = len(mypaths)
                if noofpaths in noofpathsperarticle: 
                    noofpathsperarticle[noofpaths] += 1
                else: 
                    noofpathsperarticle[noofpaths] = 1
                for goodpath in mypaths: 
                    a =  0
                    #idoutputfile.write("*%s (%s)\n" %(goodpath.path, goodpath.score))
        notgradedfile.close()
    idoutputfile.close()
    p("Articles not graded for %s is %d" %(letter, len(articles_not_graded)), "info")

p("Number of paths found for all articles", "info")
with open("noofpaths.txt", "w") as pathfile: 
    for number in noofpathsperarticle: 
        pathfile.write("%s\t%d\n" %(number, noofpathsperarticle[number]))
pathfile.close()
gc.collect()
