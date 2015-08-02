import gzip, re
from myprint import myprint as p
from unidecode import unidecode

inputfilename = "no-mapping.txt.gz"
categoryinputfilename = "enwiki-latest-categorylinks.sql.gz"
redirectinputfilename = "output-redirect-titles.txt.gz"
pagefilename = "enwiki-latest-page.sql.gz"

nopages = dict()
redirects = dict()
pages = dict()

p("Reading %s" %(inputfilename), "info")
with gzip.open(inputfilename, "rb") as inputfile: 
    for line in inputfile: 
        line = line.strip()
        line = line.lower()
        splittet = line.split("\t")
        if len(splittet) < 2: 

            continue
        nopages[splittet[0]] = splittet[1]

inputfile.close()
p("Finished reading %s" %(inputfilename), "info")

p("Reading %s" %(redirectinputfilename), "info")
with gzip.open(redirectinputfilename, "rb") as redirectfile:
    for line in redirectfile:     
        #line = unicode(line, "utf-8")
        line.decode('utf-8', 'ignore')
        line = line.lower()
        split_line = line.split(",")
        pageid = split_line[0]
        pagename = split_line[1]
        #if category not in redirects:
        redirects[pageid] = pagename
p("Finsihed readling %s" %(redirectinputfilename), "info")

def is_number (input):
    try:
        int(input)
        return True
    except:
        return False

pages = dict()
with gzip.open("pages-en.txt.gz", "rb") as eninputfile: 
    for line in eninputfile: 
        line = line.strip()
        splittet = line.split("\t")
        if len(splittet) < 2: 
            continue
        pages[splittet[0]] = splittet[1]

entono = dict()
for insertion_id in pages: 
    if insertion_id in nopages: 
        entono[pages[insertion_id]] = nopages[insertion_id]

outputfilename = "en-to-no.txt.gz"
p("Writing results to %s" %(outputfilename), "info")
with gzip.open(outputfilename, "wb") as entonofile: 
    for en_name in entono: 
        outen_name = en_name
        try:
            outen_name = outen_name.decode('unicode-escape')
        except SyntaxError: 
            outen_name = outen_name.decode('ascii')       
        try: 
            outen_name = unidecode(outen_name)
        except: 
            a = 0
        outen_name = outen_name.lower()    
        outno_name = entono[en_name]
        entonofile.write("%s\t%s\n" %(en_name, outno_name))

entonofile.close()
