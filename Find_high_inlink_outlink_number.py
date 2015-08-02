import gzip

"""
Program to find the highest inlink and outlink numbers for all categories. 
Small modifications of this program can be used to find average inlink/outlink number
"""

inputfilename = "Subcat-links.txt.gz"
maxinlink = 0
maxcat = ""
outlinks = dict()
inlinks = dict()
subcat = ""
with gzip.open(inputfilename, "rb") as inputfile: 
    for line in inputfile: 
        line = line.strip()
        
        splittet = line.split("\t")
        fromcategory = splittet[0]
        tocategory = splittet[1]
        
        if tocategory in inlinks: 
            if fromcategory not in inlinks[tocategory]: 
                inlinks[tocategory].append(fromcategory)
        else: 
            inlinks[tocategory] = [fromcategory]

        if fromcategory in outlinks: 
            if tocategory not in outlinks[fromcategory]: 
                outlinks[fromcategory].append(tocategory)
        else: 
            outlinks[fromcategory] = [tocategory]

for subcat in inlinks: 
    if len(inlinks[subcat]) > maxinlink: 
        maxinlink = len(inlinks[subcat])
        maxcat = subcat

print maxcat
print maxinlink
print inlinks[maxcat]

maxoutlink = 0
maxoutcat = ""
for subcat in outlinks: 
    if len(outlinks[subcat]) > maxoutlink: 
        maxoutlink = len(outlinks[subcat])
        maxoutcat = subcat

print outlinks[maxoutcat]
print maxoutcat
print maxoutlink
