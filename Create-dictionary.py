# -*- coding: utf-8 -*-
import gzip, json, yaml, io
from myprint import myprint as p

"""
Program for creating a dictionary for a dictionary-based classifier
for another language (based on the English dictionary)
"""

nomappingfilename = "no-mapping.txt.gz"

nomapping = dict()
p("Reading %s" %(nomappingfilename), "info")
with gzip.open(nomappingfilename, "rb") as nomappingfile: 
    for line in nomappingfile: 
        line = line.strip()
        splittet = line.split("\t")
        if len(splittet) < 2: 
            continue
        nomapping[splittet[0]] = splittet[1]
nomappingfile.close()

entrytoidfilename = "en-entry-to-pageid.json"
p("Reading %s" %(entrytoidfilename), "info")
with open(entrytoidfilename, "rb") as inputfile:
    entrypageid = yaml.load(inputfile)
p("finished reading python json", "info")

norwegianstopwords = []
stopwordfile = "norwegian_stop_words.txt"
with open(stopwordfile, "r") as inputfile: 
    for line in inputfile: 
        line = line.strip()
        norwegianstopwords.append(line)
        
latestversion = 5
iggdictionary = dict()
dictionaryfilename = "clean-igg-dictionary-" + str(latestversion) +".json"
iggiabtaxonomy = "igg-iabtaxonomy" + str(latestversion)
p("Reading dictionary", "info")
with open(dictionaryfilename, "rb") as inputfile:
    dictionary = yaml.load(inputfile)
p("finished reading python json", "info")
endictionary = dictionary[iggiabtaxonomy]

nodictionary = dict()
for entry in entrypageid: 
    pageids = entrypageid[entry]
    foundnorwegian = False
    onlyone = True
    norwegianentry = ""
    for pageid in pageids: 
        if pageid in nomapping: 
            if foundnorwegian: 
                onlyone = False
                continue

            foundnorwegian = True
            norwegianentry = nomapping[pageid]
    if foundnorwegian and onlyone: 

        # Check if the norwegian entry is ambiguous
        if "(" in norwegianentry: 
            print "Ambiguous norwegian entry: %s" %norwegianentry
            continue
        
        # Check if the norwegian entry is in the norwegian stopwordlist: 
        if norwegianentry in norwegianstopwords:
            print "Norwegian entry in stopword list: %s" %norwegianentry
            continue
        for entryword in norwegianentry.split(" "):
            if entryword in norwegianstopwords: 
                print "Norwegian stopword in the entry: %s" %norwegianentry
                continue         
        if "\\'" in norwegianentry: 
            norwegianentry = norwegianentry.replace("\\'", "'")
        nodictionary[norwegianentry] = endictionary[entry]
            
noiggdictionary = dict()
noiggdictionary["igg-noiabtaxonomy1"] = nodictionary
noiggdictionary["global-properties"] = dict()
noiggdictionary["global-properties"]["annotate-paths"]="false",
noiggdictionary["global-properties"]["count"]="2",
noiggdictionary["global-properties"]["count-field"]="value",
noiggdictionary["global-properties"]["expand-paths"]="true",   
noiggdictionary["global-properties"]["key-normalization-flags"]="4",
noiggdictionary["global-properties"]["leftmost-longest-match"]="true",
noiggdictionary["global-properties"]["mode"]="overlap",
noiggdictionary["global-properties"]["swap-fields"]="true",
noiggdictionary["global-properties"]["tokenizer-context"]="en",
noiggdictionary["global-properties"]["unique-count"]="2",
noiggdictionary["global-properties"]["value-normalization-flags"]="4"

with io.open("igg-dictionary-no.json", 'w', encoding='utf8') as json_file:
    data = json.dumps(noiggdictionary, ensure_ascii=False, encoding='utf8', indent=2)
    json_file.write(unicode(data))

print "Norwegian entry list with %d entries" %(len(nodictionary))
