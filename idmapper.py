import gzip

names = dict()      # Dictionary to keep track of the ids to the names
ids = dict()        # Dictionary to keep track of the names to the ids
namecnt = 0

# Method that returns the id of the name
def name_to_id(name):
    global names
    return names[name]

# Method to insert a name in the dictionary 'names'
# Name is only added if its not already in the dictionary
def insert_name(name):
    global namecnt
    global names
    global ids
    if name not in names:
        names[name] = namecnt
        ids[namecnt] = name
        namecnt+= 1

# Method that returns the id of the name
# Returns -1 if the name is not present
def id_to_name(nameid):
    global ids
    if nameid in ids:
        return ids[nameid]
    else:
        return -1

# Method for writing the results of the idmapper to file
# File is written compressed
def idmapper_to_file():
    global ids
    global names
    with gzip.open("id-mapper.txt.gz", "wb") as idfile:
        for myid in ids:
            idfile.write("%d, %s\n" %(myid, ids[myid]))

    idfile.close()
