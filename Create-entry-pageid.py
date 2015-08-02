# -*- coding: utf-8 -*-
import gzip, json, yaml, io
from myprint import myprint as p

"""
Program for a file containing all dictionary entries and what page ids they are based on.
Sorts out all relevant dictionary entries based on the latest version of the igg-iabtaxonomy

Why? Because the file containing all possible entries and their page ids is extremely large.

Input: A file containing all processed Wikipedia article pages and their corresponding ids
Output: A file continaing the relevant dictionary entries and what page ids they are based on
"""

# Reading the English
enmappingfilename = "pageid-pagetitle-en.txt.gz"
enpagetitle_to_id = dict()
p("Reading %s" %(enmappingfilename), "info")
with gzip.open(enmappingfilename, "rb") as enmappingfile: 
    for line in enmappingfile: 
        line = line.strip()
        splittet = line.split("\t")
        if len(splittet) < 2: 
            continue
        pageid = splittet[0]
        pagetitle = splittet[1]
        if pagetitle in enpagetitle_to_id:
            enpagetitle_to_id[pagetitle].append(pageid)
        else: 
            enpagetitle_to_id[pagetitle] = [pageid]
enmappingfile.close()


latestversion = 5                                      # Latest version, update for later versions
iggiabversion = "igg-iabtaxonomy" + str(latestversion) # Name of the igg-iabtaxonomy
inputfilename = "clean-igg-dictionary-" + str(latestversion) + ".json" # Inputfilename
p("Reading %s" %(inputfilename), "info")
with open(inputfilename, "rb") as inputfile:
    iggdictionary = yaml.load(inputfile)
p("finished reading python json", "info")

dictionary = iggdictionary[iggiabversion]

entry_to_pageid = dict()

for entry in dictionary: 
    if entry in enpagetitle_to_id: 
        pageids = enpagetitle_to_id[entry]
        
        entry_to_pageid[entry] = pageids

with io.open("en-entry-to-pageid.json", 'w', encoding='utf8') as json_file:
    data = json.dumps(entry_to_pageid, ensure_ascii=False, encoding='utf8', indent=2)
    json_file.write(unicode(data))
