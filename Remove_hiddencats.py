# -*- coding: utf-8 -*-

import sys, os, numpy, re, fileinput, gzip, gc, time, Queue
from myprint import myprint as p
from itertools import islice
from unidecode import unidecode

"""
Program to remoce hidden categories from the category graph.
The program takes the name of all hidden categories and the category graph as input.
We have a method that recursively find all visible children of a category.
First we go through all the hidden categories and find their visible children, all computations
are stored so we don't have to find the children of hidden category again.
Then we go though all visible categories and add all their visible children and the visible
children of the hidden categories.
"""

try:
    categoryinputfilename = sys.argv[1]
    hiddencategoryinputfilename = sys.argv[2]
    outputfilename = sys.argv[3]
except:
    print "\n[RUN]: \n"\
    "python Remove_hiddencats.py \n"\
    "\t [Sub-categories-new.txt.gz]\n"\
    "\t [All_hidden_categories.txt.gz]\n"\
    "\t [Subcat-links.txt.gz\n\n"\
    "[FUNC:] Split the categorylink-file to the categories concerning pages and those concerning sub categories. Skip all hidden categories to remove number of relevant category links.\n"
    exit(0)

allcategories = dict()  #Dictionary to keep track of all categories
hidden_cat = dict()     #Dictionary to keep track of all hidden categories
links = dict()          #Dictionary to keep track of all links in the graph
artskip = catskip = hiddencnt = 0

starttime = time.time()

# Reads all the hidden categories from the file
p("Reading all hidden categories", "info")
with gzip.open(hiddencategoryinputfilename, "rb") as hiddencategories:
    for line in hiddencategories:
        line = line.strip().lower()

        # Code for representing the category names in same encoding
        try:
            line = line.decode('unicode-escape')
        except SyntaxError:
            line = line.decode('ascii')
        except Exception,e:
            a = 0

        try:
            line = unidecode(line)
        except UnicodeEncodeError, e:
            print str(e)
            print line
        except Exception,e:
            print str(e)
            print line
        line = line.lower()

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
        # Code for representing the category names in same encoding

        try:
            line = line.decode('unicode-escape')
        except SyntaxError:
            line = line.decode('ascii')
        except Exception,e:
            a = 0

        try:
            line = unidecode(line)
        except UnicodeEncodeError, e:
            print str(e)
            print line
        except Exception,e:
            print str(e)
            print line
        line = line.strip().lower()
        lines = line.split("\t")
        if len(lines) < 2:
            print lines
            continue
        parentcat = lines[0]
        subcat = lines[1]

        # The supercategory is added to  allcategories if not present
        if parentcat not in allcategories:
            allcategories[parentcat] = 1
        # The subcategory is added to allcategories if not present
        if subcat not in allcategories:
            allcategories[subcat] = 1

        if parentcat == "" or subcat == "":
            continue

        # Links between supercategory and subcategory is stored
        if parentcat in links:
            links[parentcat].append(subcat)
        else:
            links[parentcat] = [subcat]
p("Number of categories: %d" %(len(links)), "info")
inputfile.close()

nothidden = dict()      #Dictionary to store all visible categories
hidden = dict()         #Dictionary to store all hidden categories

# Looping through all category links
for category in links:
    if category in hidden_cat:
        # Category is stored as hidden if it's a hidden category
        hidden[category] = 1
    else:
        # Category is stored as visible if it's not a hidden category
        nothidden[category] = 1

linksremoved = 0
mychildren = dict()     #Dictionary to keep track of all children of a category
found = dict()          #Dictionary to keep track of all categories visited


# Method to recursively find all visbile childen of a category
def find_all_children(category):
    global found
    global mychildren
    if category in found:
        # if the category is already visited, return all children found
        return mychildren
    # Store children as the links from the category
    children = links[category]
    # Looping through all the children
    for child in children:
        if child in found:
            # If child is already visited, it's skipped
            continue
        found[child] = 1   # child is set to visited
        if child in nothidden:
            # If the child is visible: add to mychildren
            mychildren[child] = 1
        else:
            # The child is a hidden category
            if child in links:
                # If the child has links to other categories:
                # Find all children of the child and add them to mychildren
                morechildren = find_all_children(child)
                for morechild in morechildren:
                    mychildren[morechild] = 1
    return mychildren


newhidden = dict()          #Dictionary to save all the visible children of a hidden category
                            #This is to save old computations.

p("Not hidden categories: %d" %(len(nothidden)), "info")
p("Hidden categories: %d" %(len(hidden)), "info")

# Looping through all hidden categories
for category in hidden:
    if category == "hidden categories":
        # if it's the main hidden category: skip
        newhidden[category] = []
        continue
    mychildren = dict()     #Dictionary to keep track of all children of a category
    found = dict()          #Dictionary to keep track of all categories visited
    children = links[category]
    found[category] = 1
    allchildren = []        #List to keep track of all visible children of a category
    for child in children:
        if child in hidden:
            if child not in newhidden:
                # If the child is a hidden category and we have not found all its children
                mychildren = find_all_children(child)
            else:
                mycildren = newhidden[child]
            for mychild in mychildren:
                if mychild not in allchildren:
                    allchildren.append(mychild)
            linksremoved+=1
        elif child not in allchildren:
            allchildren.append(child)
    newhidden[category] = allchildren # Add our computations so we don't have to recompute

p("Number of links removed: %d" %(linksremoved), "info")

allcategoriesafter = dict() #Dictionary to store the final results without hidden cats

# Find all categories after hidden categories are removed
# Write the new category graph to file
with gzip.open(outputfilename, "wb") as outputfile:
    for category in nothidden:
        # Add the nonhidden categories to allcategoriesafter
        if category not in allcategoriesafter:
            allcategoriesafter[category] = 1

        mychildren = dict()     #Dictionary to keep track of all children of a category
        found = dict()          #Dictionary to keep track of all categories visited
        found[category] = 1     # Set category as visited

        children = links[category]
        links.pop(category, None)
        newchildren = []
        # Go through all children of the category
        for child in children:
            if child in hidden:
                # If child is hidden, we store its visible children as the cat's children
                newchildren = newhidden[child]
                for newchild in newchildren:
                    if newchild not in allcategoriesafter:
                        allcategoriesafter[newchild] = 1
                    outputfile.write("%s\t%s\n" %(category, newchild))
            else:
                if child not in allcategoriesafter:
                    allcategoriesafter[child] = 1

                outputfile.write("%s\t%s\n" %(category, child))
        nothidden[category] = newchildren
outputfile.close()

p("All categories after: %d" %(len(allcategoriesafter)), "info")
p("All hidden categories removed", "info")
p("Total time: %.3f min" %((time.time()-starttime)/60), "info")
gc.collect()
