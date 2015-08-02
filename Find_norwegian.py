import gzip, re

"""
Program to find all Norwegian links in Wikipedia
"""

inputfilename = "enwiki-latest-langlinks.sql.gz"
nomapping = dict()
with gzip.open(inputfilename, "rw") as inputfile: 
    for line in inputfile: 
        line = line.strip()
        if line.startswith("INSERT") == False: 
            continue      
        line = line[31:]
        regex = "\(((\d+)\,\'(\w+)\'\,\'(.*?))\'\)"
        insertions = re.findall(regex, line)
        for insertion in insertions: 
            language = insertion[2]
            if language == "no":
                nomapping[insertion[1]] = insertion[3]

with gzip.open("no-mapping.txt.gz", "wb") as outputfile: 
    for langlink in nomapping: 
        outputfile.write("%s\t%s\n" %(langlink, nomapping[langlink]))
outputfile.close()

print "All no-links found: %d" %(len(nomapping))
                         
