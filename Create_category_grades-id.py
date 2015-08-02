from __future__ import division

import sys, os, numpy, re, fileinput, gzip, gc, time, Queue
from myprint import myprint as p
import idmapper

"""
Program for creating category grades. 
The program uses ids to create the category grades. 
"""

try: 
    categoryinfofilename = sys.argv[1]
    categoriesoutputfilename = sys.argv[2]
except: 
    print "\n[RUN]: \n"\
    "python Number_of_parents.py \n"\
    "\t [category-info.txt]\n"\
    "\t [category-parents.txt.gz]\n\n"\
    "[FUNC:]\n"\
    "Finding number of parents for each catgory."\
    " and finding the grade for each category \n"
    exit(0)

grades = dict()

C_in = C_out = 0
avg_in = avg_out = 0
def create_grades(): 
    global grades
    global C_in
    global C_out
    global avg_in
    global avg_out
    for category in grades: 
        inlink = grades[category][1]
        outlink = grades[category][0]
        grade = (inlink + outlink + 0.0)/(avg_in + avg_out)
        grades[category] = grade
        grades[category]
        
id_to_name = dict()
name_to_id = dict()
def read_ids(idfilename): 
    with gzip.open(idfilename) as idfile: 
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
    p("Read all ids", "info")
    idfile.close()

def find_grades(categoryinfofilename, categoriesoutputfilename): 
    global grades
    global C_in
    global C_out
    global avg_in
    global avg_out
    starttime = time.time()
    begintime = starttime
    p("Reading all category info", "info")
    parent = child = ""
    graph = dict()    # Dictionary to keep track of the children to each parent cat
    subgraph = dict() # Dictionary to keep track of the parents of each cat
    
    # Creating category graph
    
    with open(categoryinfofilename) as categorygraph:
        for line in categorygraph:
            line = line.strip()
            if line.startswith("*"): #children
                child = name_to_id[line[2:]]
                if parent == "":
                    continue
                if parent in graph:
                    if child not in graph[parent]: 
                        graph[parent].append(child)
                else:
                    graph[parent] = [child]

                if child in subgraph: 
                    if parent in subgraph[child]: 
                        a = 0
                    else: 
                        subgraph[child].append(parent)
                else: 
                    subgraph[child] = [parent]

            else:
                line = line.replace("_", " ")
                parent = name_to_id[line]
            #idmapper.insert_name(parent)
                
    p("Finished reading all info [Time: %s sec]" %(time.time()-starttime), "info")
    maxparent = maxchildren = outlinks = inlinks = 0
    mparent = mchildren = ""
    
    C_in = len(subgraph)
    C_out = len(subgraph)
    for category in graph: 
        if len(graph[category])> maxchildren: 
            maxchildren = len(graph[category])
            mchildren = category
        outlinks+= len(graph[category])
        
        grades[category] = [len(graph[category])]

        if category in subgraph:
            
            grades[category].append(len(subgraph[category]))
            
            inlinks += len(subgraph[category])
            if len(subgraph[category]) > maxparent: 
                maxparent = len(subgraph[category])
                mparent = category
            """
                if (len(graph[category]) > 10) and (len(subgraph[category]) > 10): 
                cnt10+= 1
            if (len(graph[category]) > 20) and (len(subgraph[category]) > 20): 
                cnt20+= 1
            if (len(graph[category]) > 30) and (len(subgraph[category]) > 30): 
                cnt30+= 1
            if (len(graph[category]) > 40) and (len(subgraph[category]) > 40): 
                cnt40+= 1
            if (len(graph[category]) > 50) and (len(subgraph[category]) > 50): 
                cnt50+= 1
            if (len(graph[category]) > 60) and (len(subgraph[category]) > 60): 
                cnt60+= 1
            if (len(graph[category]) > 70) and (len(subgraph[category]) > 70): 
                cnt70+= 1
            if (len(graph[category]) > 80) and (len(subgraph[category]) > 80): 
                cnt80+= 1
            if (len(graph[category]) > 90) and (len(subgraph[category]) > 90): 
                cnt90+= 1
            if (len(graph[category]) > 100) and (len(subgraph[category]) > 100): 
                cnt100+= 1
                print "category: %s, number: %d\n" %(category, len(graph[category]))
                """
                #print "%s: %d, %d\n" %(category, len(graph[category]), len(subgraph[category]))
            #outputfile.write("%s: %d, %d\n" %(category, len(graph[category]), len(subgraph[category])))
            subgraph.pop(category, None)
        else: 
            grades[category].append(0)
            #outputfile.write("Only children: %s: %d\n" %(category, len(graph[category])))
    for category in subgraph: 
        grades[category] = [0, len(subgraph[category])]
        inlinks += len(subgraph[category])

    avg_in = inlinks / C_in
    avb_out = outlinks / C_out
        #outputfile.write("Only parents: %s: %d\n" %(category, len(subgraph[category])))
    #return create_grades()
#outputfile.close()
"""
thresholds = [10, 20, 30, 40, 50]
p("Number of categories with %d parent categories and subcategories: %d" %(10, cnt10), "info")
p("Number of categories with %d parent categories and subcategories: %d" %(20, cnt20), "info")
p("Number of categories with %d parent categories and subcategories: %d" %(30, cnt30), "info")
p("Number of categories with %d parent categories and subcategories: %d" %(40, cnt40), "info")
p("Number of categories with %d parent categories and subcategories: %d" %(50, cnt50), "info")
p("Number of categories with %d parent categories and subcategories: %d" %(60, cnt60), "info")
p("Number of categories with %d parent categories and subcategories: %d" %(70, cnt70), "info")
p("Number of categories with %d parent categories and subcategories: %d" %(80, cnt80), "info")
p("Number of categories with %d parent categories and subcategories: %d" %(90, cnt90), "info")
p("Number of categories with %d parent categories and subcategories: %d" %(100, cnt100), "info")

p("Maxparent: %d (%s)" %(maxparent, mparent), "info")
p("Maxchildren: %d (%s)" %(maxchildren, mchildren), "info")
#subcats = graph["2015"]
#for s in subcats: 
#    print s

p("C_out: %d" %(C_out), "info")
p("C_in: %d" %(C_in), "info")
p("Inlinks: %d, give inlink_avg: %d\n" %(inlinks, inlinks/C_out), "info")
p("Outlinks: %d, outlinnk_avg: %d\n" %(outlinks, outlinks/C_in), "info")
"""
read_ids("id-mapper.txt.gz")
find_grades(categoryinfofilename, categoriesoutputfilename)
create_grades()
p("Writing all grades to file", "info")
with gzip.open("category-grade.txt.gz", "wb") as gradefile:
    for category in grades: 
        #print grades[category]
        gradefile.write("%s\t%f\n" %(category, grades[category]))

gradefile.close()
                       
# High grade is bad. 
