import sys, os, numpy, re, fileinput, gzip, gc
from myprint import myprint as myprint

"""
Program to create a category graph from the links between categories.
"""

try:
    categoryinputfilename = sys.argv[1]
    categoryoutputfilename = sys.argv[2]
except:
    print "\n\n[RUN]: \n"\
        "python Categorygraph_builder.py \n"\
        "\t [Sub-categories.txt.gz]\n"\
        "\t [category-info.txt]\n\n"\
    "[FUNCTION]: \n"\
    "Create a category graph from all the links between categories\n"
    exit(0)


sub_categories = dict() #Dictionary to store the graph, supercategory link to subcategory
categorycnt = catcnt = subcatteller = 0

# Reads the links between categories and create the graph
myprint("Reading content...", "info")
with gzip.open(categoryinputfilename) as inputfile:
    for line in inputfile:
        words = line.split("\t")

        parent_category = words[0].lower().strip()
        sub_category = words[1].lower().strip()

        # If the link is incomplete, we skip it
        if parent_category == " " or parent_category == "":
            continue
        elif sub_category == " " or sub_category == "":
            continue

        catcnt += 1
        if parent_category in sub_categories:
            # Supercategory is in the graph, subcategory is added to the graph
            sub_categories[parent_category][sub_category] = 1
        else:
            # Supercategory and subcategory is added to the graph
            sub_categories[parent_category] = dict()
            sub_categories[parent_category][sub_category] = 1
            categorycnt += 1

# Writes the graph to file
myprint("Writing categories graph to file...", "info")
with open(categoryoutputfilename, 'w') as categoryoutput:
    for categorytitle in sub_categories:
        categoryoutput.write("%s\n" %(categorytitle))
        for category in sub_categories[categorytitle]:
            categoryoutput.write("* %s \n" %(category))
categoryoutput.close()
myprint("%d supercategories written to %s" %(categorycnt, categoryoutputfilename), "info")
gc.collect()
