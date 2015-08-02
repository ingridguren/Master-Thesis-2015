import gzip, re
from myprint import myprint as p
from unidecode import unidecode

"""
Program for finding the pageid for an entry.
Needs to do the same process as the mapper so that the entries are identical.
"""


categoryinputfilename = "enwiki-latest-categorylinks.sql.gz"
redirectinputfilename = "output-redirect-titles.txt.gz"
pagefilename = "enwiki-latest-page.sql.gz"

redirects = dict()
pageid_to_title = dict()
pagetitle_to_id = dict()

"""
p("Reading %s" %(inputfilename), "info")
with gzip.open(inputfilename, "rb") as inputfile: 
    for line in inputfile: 
        line = line.strip()
        line = line.lower()
        splittet = line.split("\t")
        if len(splittet) < 2: 
            #print "< 2: " + line
            continue
        nopages[splittet[0]] = splittet[1]

inputfile.close()
p("Finished reading %s" %(inputfilename), "info")
"""
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

teller = 0
categorycnt = 0
pagecnt = 0
p("Reading content from %s" %(categoryinputfilename), "info")
with gzip.open(categoryinputfilename) as inputfile: 
    for line in inputfile:
        if (line.startswith("INSERT")):
            teller+=1
            if (teller % 10) == 0:
                print "%d - %d \n" %(categorycnt, pagecnt)
            line = line[35:]
            line = line.lower()
            regex = "(\(\d+\,.*?\,('file'|'page'|'subcat')\))"
            
            insertions = re.findall(regex, line)
            for insertion in insertions:
                insertion = insertion[0]

                words = insertion.split("','")
                words[0] = words[0][1:]
                words[-1] = words[-1][:-1]

                insertion_id = words[0].split(",")[0]
                from_link = words[0].split(insertion_id)[1][2:]
                to_link = words[1]

                if insertion_id in redirects:
                    before = to_link
                    to_link = redirects[insertion_id]

                if words[-1] == "page'": 
                    page_name = to_link.replace("_", " ")
                    if is_number(page_name):
                        continue

                    if "\\n" in page_name:
                        page_split = page_name.split("\\n")
                        if page_split[0] == page_split[1]:
                            page_name = page_split[0]
                        elif page_split[0] == "":
                            page_name = page_split[1]
                        elif page_split[1] == "":
                            page_name = page_split[0]
                        elif "," in page_name:
                            page_name = page_split[1]
                        elif len(page_split[0]) > len(page_split[1]):
                            page_name = page_split[0]
                        else:
                            page_name = page_split[1]
                            pagecnt += 1
                    pageid_to_title[insertion_id] = page_name


freqlist = ["a","about","above","across","act","active","activity","add","afraid","after","again","age","ago","agree","air","all","alone","along","already","always","am","amount","an","and","angry","another","answer","any","anyone","anything","anytime","appear","apple","are","area","arm","army","around","arrive","art","as","ask","at","attack","aunt","autumn","away","baby","back","bad","bag","ball","bank","base","basket","bath","be","bean","bear","beautiful","bed","bedroom","beer","before","begin","behave","behind","bell","below","besides","best","better","between","big","bird","birth","birthday","bit","bite","black","bleed","block","blood","blow","blue","board","boat","body","boil","bone","book","border","born","borrow","both","bottle","bottom","bowl","box","boy","branch","brave","bread","break","breakfast","breathe","bridge","bright","bring","brother","brown","brush","build","burn","bus","business","busy","but","buy","by","cake","call","can","candle","cap","car","card","care","careful","careless","carry","case","cat","catch","central","century","certain","chair","chance","change","chase","cheap","cheese","chicken","child","children","chocolate","choice","choose","circle","city","class","clean","clear","clever","climb","clock","close","cloth","clothes","cloud","cloudy","coat","coffee","coin","cold","collect","colour","comb","come","comfortable","common","compare","complete","computer","condition","contain","continue","control","cook","cool","copper","corn","corner","correct","cost","count","country","course","cover","crash","cross","cry","cup","cupboard","cut","dance","dangerous","dark","daughter","day","dead","decide","decrease","deep","deer","depend","desk","destroy","develop","die","different","difficult","dinner","direction","dirty","discover","dish","do","dog","door","double","down","draw","dream","dress","drink","drive","drop","dry","duck","dust","duty","each","ear","early","earn","earth","east","easy","eat","education","effect","egg","eight","either","electric","elephant","else","empty","end","enemy","enjoy","enough","enter","entrance","equal","escape","even","evening","event","ever","every","everybody","everyone","exact","examination","example","except","excited","exercise","expect","expensive","explain","extremely","eye","face","fact","fail","fall","false","family","famous","far","farm","fast","fat","father","fault","fear","feed","feel","female","fever","few","fight","fill","film","find","fine","finger","finish","fire","first","fit","five","fix","flag","flat","float","floor","flour","flower","fly","fold","food","fool","foot","football","for","force","foreign","forest","forget","forgive","fork","form","four","fox","free","freedom","freeze","fresh","friend","friendly","from","front","fruit","full","fun","funny","furniture","further","future","game","garden","gate","general","gentleman","get","gift","give","glad","glass","go","goat","god","gold","good","goodbye","grandfather","grandmother","grass","grave","great","green","grey","ground","group","grow","gun","hair","half","hall","hammer","hand","happen","happy","hard","hat","hate","have","he","head","healthy","hear","heart","heaven","heavy","height","hello","help","hen","her","here","hers","hide","high","hill","him","his","hit","hobby","hold","hole","holiday","home","hope","horse","hospital","hot","hotel","hour","house","how","hundred","hungry","hurry","hurt","husband","ice","idea","if","important","in","increase","inside","into","introduce","invent","invite","iron","is","island","it","its","jelly","job","join","juice","jump","just","keep","key","kill","kind","king","kitchen","knee","knife","knock","know","ladder","lady","lamp","land","large","last","late","lately","laugh","lazy","lead","leaf","learn","leave","left","leg","lend","length","less","lesson","let","letter","library","lie","life","light","like","lion","lip","list","listen","little","live","lock","lonely","long","look","lose","lot","love","low","lower","luck","machine","main","make","male","man","many","map","mark","market","marry","matter","may","me","meal","mean","measure","meat","medicine","meet","member","mention","method","middle","milk","million","mind","minute","miss","mistake","mix","model","modern","moment","money","monkey","month","moon","more","morning","most","mother","mountain","mouth","move","much","music","must","my","page","pain","paint","pair","pan","paper","parent","park","part","partner","party","pass","past","path","pay","peace","pen","pencil","people","pepper","per","perfect","period","person","petrol","photograph","piano","pick","picture","piece","pig","pin","pink","place","plane","plant","plastic","plate","play","please","pleased","plenty","pocket","point","poison","police","polite","pool","poor","popular","position","possible","potato","pour","power","present","press","pretty","prevent","price","prince","prison","private","prize","probably","problem","produce","promise","proper","protect","provide","public","pull","punish","pupil","push","put","queen","question","quick","quiet","quite","radio","rain","rainy","raise","reach","read","ready","real","really","receive","record","red","remember","remind","remove","rent","repair","repeat","reply","report","rest","restaurant","result","return","rice","rich","ride","right","ring","rise","road","rob","rock","room","round","rubber","rude","rule","ruler","run","rush","sad","safe","sail","salt","same","sand","save","say","school","science","scissors","search","seat","second","see","seem","sell","send","sentence","serve","seven","several","sex","shade","shadow","shake","shape","share","sharp","she","sheep","sheet","shelf","shine","ship","shirt","shoe","shoot","shop","short","should","shoulder","shout","show","sick","side","signal","silence","silly","silver","similar","simple","since","sing","single","sink","sister","sit","six","size","skill","skin","skirt","sky","sleep","slip","slow","small","smell","smile","smoke","snow","so","soap","sock","soft","some","someone","something","sometimes","son","soon","sorry","sound","soup","south","space","speak","special","speed","spell","spend","spoon","sport","spread","spring","square","stamp","stand","star","start","station","stay","steal","steam","step","still","stomach","stone","stop","store","storm","story","strange","street","strong","structure","student","study","stupid","subject","substance","successful","such","sudden","sugar","suitable","summer","sun","sunny","support","sure","surprise","sweet","swim","sword","table","take","talk","tall","taste","taxi","tea","teach","team","tear","telephone","television","tell","ten",\
#"tennis",
"terrible","test","than","that","the","their","then","there","therefore","these","thick","thin","thing","think","third","this","though","threat","three","tidy","tie","title","to","today","toe","together","tomorrow","tonight","too","tool","tooth","top","total","touch","town","train","tram","travel","tree","trouble","true","trust","try","turn","twice","type","uncle","under","understand","unit","until","up","use","useful","usual","usually","vegetable","very","village","visit","voice","wait","wake","walk","want","warm","wash","waste","watch","water","way","we","weak","wear","weather","wedding","week","weight","welcome","well","west","wet","what","wheel","when","where","which","while","white","who","why","wide","wife","wild","will","win","wind","window","wine","winter","wire","wise","wish","with","without","woman","wonder","word","work","world","worry","worst","write","wrong","year","yes","yesterday","yet","you","young","your","zero","zoo"\
"a", "about", "all", "and", "are", "as", "at", "back", "be", "because", "been", "but", "can", "can't", "come", "could", "did", "didn't", "do", "don't", "for", "from", "get", "go", "going", "good", "got", "had", "have", "he", "her", "here", "he's", "hey", "him", "his", "how", "I", "if", "I'll", "I'm", "in", "is", "it", "it's", "just", "know", "like", "look", "me", "mean", "my", "no", "not", "now", "of", "oh", "OK", "okay", "on", "one", "or", "out", "really", "right", "say", "see", "she", "so", "some", "something", "tell", "that", "that's", "the", "then", "there", "they", "think", "this", "time", "to", "up", "want", "was", "we", "well", "were", "what", "when", "who", "why", "will", "with", "would", "yeah", "yes", "you", "your", "you're"]

disambiguation = dict()
with open("disambiguation-titles.txt", "r") as disambgfile: 
    for line in disambgfile:
        line = line.strip()
        disambiguation[line] = 1
disambgfile.close()


"""
with gzip.open("pages-en.txt.gz", "rb") as eninputfile: 
    for line in eninputfile: 
        line = line.strip()
        splittet = line.split("\t")
        if len(splittet) < 2: 
            continue
        pageid_to_title[splittet[0]] = splittet[1]
"""
paraentries = dict()
dictionary = dict()

yearregex = "(\d\d\d\d)"
parenthesisregex = "(\(.*\))"
genderregex = "(men\'s|women\'s)"
for pageid in pageid_to_title: 
    entry = pageid_to_title[pageid]
    
    modified = False
    newentry = entry
    
    if "\\'" in newentry: 
        newentry = newentry.replace("\\'", "'")
        modified = True
            
    m = re.findall(parenthesisregex, newentry)
    
    if len(m) > 0:
        newentry = entry.replace(m[0], "")
        modified = True

    m = re.findall(yearregex, newentry)
    if len(m) > 0:
        for match in m:
            newentry = newentry.replace(match, "")
            modified = True
    
    m = re.findall(genderregex, newentry)
    if len(m) > 0: 
        for match in m: 
            newentry = newentry.replace(match, "")
            modified = True
            
    newentry = newentry.strip()
    if newentry == "": 
        continue
    newentry = ' '.join(newentry.split())

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
        
    if newentry in freqlist or is_number(newentry) or newentry in disambiguation: 
        continue

    # Check if any words are in freqlist: 
    for entryword in newentry.split(" "): 
        if entryword in freqlist: 
            continue
    """
    # Check if all words are in freqlist: 
    freqentry = True
    for entryword in newentry.split(" "): 
        if entryword not in freqlist:
            freqentry = False
            break
    if freqentry:
        continue
    """       
    if modified:
        dictionary[pageid] = newentry
    else:
        dictionary[pageid] = entry

with gzip.open("pageid-pagetitle-en.txt.gz", "wb") as enoutputfile: 
    for pageid in dictionary: 
        enoutputfile.write("%s\t%s\n" %(pageid, dictionary[pageid]))
enoutputfile.close()
