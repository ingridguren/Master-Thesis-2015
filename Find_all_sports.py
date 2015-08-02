import gzip

inputfilename = "category-info.txt"

subcats = []
sports = False
with open(inputfilename) as inputfile: 
    for line in inputfile: 
        line = line.strip()
        if line == "sports": 
            sports = True
            print "found sports"
            continue
        if sports: 
            if line.startswith("*") == False: 
                sports = False
                continue
            subcats.append(line[1:])

with open("sports-subcats.txt", "w") as outputfile: 
    for subcat in subcats: 
        outputfile.write("%s\n" %(subcat))

outputfile.close

artinputfile = "article-info.txt.gz"
sportarts =  []
artfound = False
with gzip.open(artinputfile, "rb") as artinputfile: 
    for line in artinputfile: 
        line = line.strip()
        if line in subcats: 
            artfound = True
            continue
        if artfound: 
            if line.startswith("*") == False: 
                artfound = False
                continue
            sportarts.append(line[1:])

with open("sports-arts.txt", "w") as outputfile: 
    for art in sportarts: 
        outputfile.write("%s\n" %(art))
