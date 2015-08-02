import sys, os, numpy, re, fileinput, gzip, gc, time, Queue, collections, json, yaml
from operator import itemgetter
from myprint import myprint as p
from unidecode import unidecode

"""
Program for cleaning the dictionary. 
All entries are cleaned to a format where their occurrences are more likely
and where similar entries are combined. 
"""

class Entry(object):
    """
    Class for representing a dictionary entry. 
    tierone: the first tiers the entry is mapped to
    oldentry: how the entry looked before it was transformed/cleaned
    newentry: the entry after the transformation/cleaning
    """
    tierone = []

    def __init__(self, oldentry, newentry, tierone): 
        
        if ("hobbies & interests" not in oldentry) \
                and ("education" not in oldentry) and ("family & parenting" not in oldentry):
            self.oldentry = oldentry
        if ("hobbies & interests" not in newentry) \
                and ("education" not in newentry) and ("family & parenting" not in newentry): 
            self.newentry = newentry

        self.tierone = tierone
        self.newentry = newentry
        self.oldentry = oldentry
        #self.entryprint()


    # Method for printing the entry, only for debugging
    def entryprint(self):
        print "Old: %s, new: %s, tierones: %s\n" %(self.oldentry, self.newentry, self.tierone) 

    # Method for comparing this object to another
    def myequal(self, obj):
        for category in obj.tierone:
            if category not in self.tierone:
                return False
        return True

inputfilename = "igg-mapping-all.txt"

version = 4                                     # Version of the dictionary to be cleaned

# Reading the dictionary
#inputfilename = "igg-dictionary-" + str(version) + ".json"
p("Reading json file", "info")
with open(inputfilename, "rb") as inputfile:
    iggdictionary = yaml.load(inputfile)        # Loading the dictionary from file
p("finished reading python json", "info")

iggiabtaxonomy = "igg-iabtaxonomy" + str(version)
dictionary = iggdictionary[iggiabtaxonomy]

newdictionary = dict()                # Dictionary for storing the final results
paraentries = dict()                  # Dictionary for keeping track on the changes made to the entries
disambiguation = dict()               # Dictionary for all disambiguation titles
disambiguationentries = dict()        # Dictionary for keeping track on all disambiguation entries

yearregex = "(\d\d\d\d)"              # Regex for recognizing years in the title
parenthesisregex = "(\(.*\))"         # Regex for recognizing parenthesis in the title
genderregex = "(men\'s|women\'s)"     # Regex for recognizing genders in the title

singleworded_arts = 0

# Reading all titles with disambiguation 
with open("all-disambiguation-titles.txt.gz", "rb") as disambgfile: 
    for line in disambgfile:
        line = line.strip()
        disambiguation[line] = 1
disambgfile.close()

# Loading common English stop words 
freqlist = []
with open("en-stopwords.txt", "r") as stopwordfile: 
    for line in stopwordfile: 
        line = line.strip()
        freqlist.append(line)
stopwordfile.close()

# Checking if myinput is a number or not
def is_number(myinput):
    try:
        int(myinput)
        return True
    except:
        return False

# Looping through all entries in the dictionary
for entry in dictionary:
    modified = False
    newentry = entry
    
    # Replacing \\' with ' if it occurs in the entry
    if "\\'" in newentry: 
        newentry = newentry.replace("\\'", "'")
        modified = True
    
    # Removing all parenthesis from the entry
    m = re.findall(parenthesisregex, newentry)
    if len(m) > 0:
        for match in m:
            newentry = entry.replace(match, "")
        modified = True

    # Removing all years from the entry
    m = re.findall(yearregex, newentry)
    if len(m) > 0:
        for match in m:
            newentry = newentry.replace(match, "")
        modified = True
    
    # Making the entry gender neutral
    m = re.findall(genderregex, newentry)
    if len(m) > 0: 
        for match in m: 
            newentry = newentry.replace(match, "")
        modified = True

    newentry = newentry.strip()
    newentry = ' '.join(newentry.split())       # Replacing multiple spaces with just one
    if newentry == "":                          # Skipping the entry if it is empty
        continue
    
    # Converting the entries to utf-8 by removing all unicode and ascii characters
    try:
        newentry = newentry.decode('unicode-escape')
    except SyntaxError: 
        newentry = newentry.decode('ascii')
    except Exception,e:
        a = 0

    try: 
        newentry = unidecode(newentry)
    except UnicodeEncodeError, e: 
        print str(e)
        print newentry
    except Exception,e: 
        print str(e)
        print newentry
    newentry = newentry.lower()
    
    # Skipping the entry if it's in the frequency list
    if newentry in freqlist: 
        #print "In frequency list:  %s " %(newentry)
        continue
    
    # Skipping the entry if it's a number
    if is_number(newentry): 
        continue

    # Skipping the entry if it's in the disambiguation list
    if newentry in disambiguation: 
        #print "In disambiguation list: %s" %(newentry)
        continue
    
    
    # Check if any words are in freqlist:
    liste = newentry.split(" ")
    myAdd = True
    for entryword in liste: 
        if entryword in freqlist: 
            myAdd = False
            continue
    
    if myAdd == False: 
        continue
       
    """
    # Check if all words are in freqlist: 
    freqentry = True
    for entryword in newentry.split(" "): 
        if entryword not in freqlist:
            freqentry = False
            break
    if freqentry:
        #print "Frequent entry: " + newentry
        continue
    """    
    
    # Adding the entry to paraentries if it's modified, directly to the newdictionary otherwise
    if modified:
        if newentry in paraentries:
            paraentries[newentry].append(entry)
        else:
            paraentries[newentry] = [entry]
    else:

        addentry = True
        if (" " not in newentry): 
            for elm in dictionary[entry]: 
                if "arts & entertainment" in elm:  
                    print "First: ", entry, "tier:", elm
                    newdictionary.pop(entry, None)
                    singleworded_arts+=1
                    addentry = False
        if addentry == True: 
            newdictionary[newentry] = dictionary[entry]


# Method for comparing all entries to see if they are identical
# Identical = same tiers and same name. 
def compare_entries(entries):
    for i in range(len(entries)):
        for j in range(len(entries)):
            if entries[i].myequal(entries[j]) == False:
                return False
    return True

# Looping through all entries that were changed
p("Looping through all entries", "info")
for entry in paraentries:
    # If only one entry was found for a entry name, it is added to the new dictionary
    if len(paraentries[entry]) < 2:
        addentry = True

        if (" " not in entry): 
            for elm in dictionary[paraentries[entry][0]]: 
                if "arts & entertainment" in elm:  
                    print "Second: ", entry, "tier:", elm
                    newdictionary.pop(entry, None)
                    singleworded_arts+=1
                    addentry = False
                    continue
        if addentry == True: 
            newdictionary[entry] = dictionary[paraentries[entry][0]]
        
    else:
        entries = []
        for oldentry in paraentries[entry]:
            tierones = []
            completetiers = []
            for tierone in dictionary[oldentry]:
                tierones.append(tierone)

            entries.append(Entry(oldentry, entry, tierones))

        equal = compare_entries(entries)

        addentry = True
        if (" " not in entry): 
            for elm in tierones: 
                if "arts & entertainment" in elm: 
                    print "Third: ", entry, "tier:", elm
                    newdictionary.pop(entry, None)
                    singleworded_arts+=1
                    addentry = False
                    print "Entry not added:", entry
        if addentry == False: 
            continue

        # All entries with the same entry name is found to be equal
        if equal:
            newdictionary[entry] = dictionary[paraentries[entry][0]]

        # The entries have different first tiers and are disregarded
        else:
            for disentry in paraentries[entry]:
                if entry in disambiguationentries:
                    disambiguationentries[entry].append(disentry)
                else:
                    disambiguationentries[entry] = [disentry]

print "Single worded arts and entertainment: ", singleworded_arts
"""
# DEBUG: For writing all ambiguous entries to file
with gzip.open("disambiguationetries.txt.gz", "wb") as disamboutputfile:
    for entry in disambiguationentries:
        outputstring = "%s: "%(entry)
        for disentry in disambiguationentries[entry]:
            outputstring = outputstring + "%s [%s]" %(disentry, dictionary[disentry])
        outputstring = outputstring + "\n"
        disamboutputfile.write(outputstring.encode('ascii', 'ignore'))
disamboutputfile.close()

# DEBUG: For writing the modified entries to file
with gzip.open("paraentries.txt.gz", "wb") as outputfile:
    for entry in paraentries:
        outputstring = "%s: %s\n" %(entry, paraentries[entry])
        outputfile.write(outputstring.encode('ascii','ignore'))
outputfile.close()
"""

iggdictionary = dict()          # The final dictionary
# Adding necessary information to the final dictionary
iggdictionary["global-properties"] = dict()
iggdictionary["global-properties"]["annotate-paths"]="false",
iggdictionary["global-properties"]["count"]="2",
iggdictionary["global-properties"]["count-field"]="value",
iggdictionary["global-properties"]["expand-paths"]="true",   
iggdictionary["global-properties"]["key-normalization-flags"]="4",
iggdictionary["global-properties"]["leftmost-longest-match"]="true",
iggdictionary["global-properties"]["mode"]="overlap",
iggdictionary["global-properties"]["swap-fields"]="true",
iggdictionary["global-properties"]["tokenizer-context"]="en",
iggdictionary["global-properties"]["unique-count"]="2",
iggdictionary["global-properties"]["value-normalization-flags"]="4"


# Denne kan fjernes om du bruker igg-iabtaxonomy2 overalt: 
iggdictionary.pop("igg-iabtaxonomy6", None)
iggdictionary.pop("igg-iabtaxonomy7", None)
iggdictionary.pop("igg-iabtaxonomy8", None)

# Adding the dictionary to the final dictionary
iggdictionary["igg-iabtaxonomy9"] = newdictionary

# Writing the final results to file
#outputfilename = "igg-iabdictionary-" + str(version) + ".json"
outputfilename = "igg-iabdictionary-9.json"
with open(outputfilename, "w") as outputfile:
    json.dump(iggdictionary, outputfile, indent=2)
