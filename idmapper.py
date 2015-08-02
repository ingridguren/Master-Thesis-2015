import gzip

names = dict()
namecnt = 0
ids = dict()

# Mapper that returns the id given a name: 
def name_to_id(name):
    global names
    return names[name]
    

def insert_name(name): 
    global namecnt
    global names
    global ids
    if name not in names: 
        names[name] = namecnt
        ids[namecnt] = name
        namecnt+= 1

# mapper that returns the name of a given id: 
def id_to_name(nameid):
    global ids
    if nameid in ids: 
        return ids[nameid]
    else: 
        return -1

def idmapper_to_file(): 
    global ids
    global names
    with gzip.open("id-mapper.txt.gz", "wb") as idfile: 
        for myid in ids: 
            idfile.write("%d, %s\n" %(myid, ids[myid]))

    idfile.close()
        

"""
# Test of names: 
testnames = ["Ingrid", "Aleksander"]
for testname in testnames:
    insert_name(testname)

# Print the test names: 
for testname in testnames:
    print "%s has id %s\n" %(testname, name_to_id(testname))

# Print the name of ids: 
print id_to_name(1) # Should be Aleksander. 

print id_to_name(4) # Should be -1 
"""
