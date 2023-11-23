#tragically, this is broken.



FILE1 = "Oxford3000"
FILENAME="Oxford5000"
FILEIRREGV="irregverbs"
FILEIRREGN="irregnouns"
FILEIRREGA="irregadj"
DATABASENAME = "lengdatabase"
DICTFILE = "dictionary"
WRITABLEFILE = "tempfile"

#test values    <<<<<<<<<<<
DATABASENAME = "testdb"
DICTFILE = "testdictionary"

import re                                           #imports regex
import json
import sqlite3

def add_word(line):
    global dictionary, dupli_key
    wordend= line.find(" ")
    word= line[:wordend].replace("\n","")
    pos= line[wordend+1:].replace("\n","").replace(".","")
    if "(" in pos:
        pos = pos[:pos.find(")")+1]
    posdata= [pos,False]
    if word not in dictionary:
        dictionary[word] = posdata
    else:
        cancelledadd = False
        origvalue= dictionary[word]
        if type(origvalue[0]) == int:
            for key in origvalue:
                altvalue = dictionary[key]
                if posdata == altvalue:
                    cancelledadd = True    #in this case, the word form is already in the dictionary
            if cancelledadd == False:      #if it is not, it can be added
                origvalue.append(dupli_key)
                dictionary.update({word:origvalue})
        elif posdata != origvalue:          #this deals with moving the original value in the dictionary
            dictionary.update({word:[dupli_key,(dupli_key+1)]}) 
            dictionary[dupli_key] = origvalue
            dupli_key +=1
        else:
            cancelledadd = True             #here the original value is the form in the dictionary
        if cancelledadd == False:           #if a new value is being added, it is done here, and the duplicate key is also incremented. 
            dictionary[dupli_key] = posdata
            dupli_key +=1

def clean_5000(f):           
    for line in f:
        line = line[:len(line)-2]                   #removes comprehension lvl
        x = line.count(",")
        if x > 0:                                   #checks for comma
            x = line.find(",")
            if x == 0:                              #if the comma is at the start of the line
                wordend= prevline.find(" ")
                prevword = prevline[:wordend]
                pos = line[1:]
            else:
                wordend= line.find(" ")
                prevword = line[:wordend]
                line1 = line[:x]+"\n"
                add_word(line1)
                pos = line[x+1:]
            line = prevword + pos
        else:
            prevline = line
        add_word(line)

def clean_3000(f):   
    delete = False
    line = 0
    pos = "####"    #pos must be initialised with a value so that the first word can be saved.
    while line < len(f):
        if delete == True:          #if delete is true, the line is not saved
            endbracket = f[line].find(")")
            if endbracket != -1:
                delete = False      #if the bracket has been closed, the program can continue to the next line
        else:                       #if the line *can* be saved, we first check whether a new bracket is opened.
            bracket = f[line].find("(")
            if bracket != -1:
                endbracket = f[line].find(")")
                if endbracket != -1:
                    delete = False  #if the bracket has been closed, the program can continue to the next line
                else:
                    delete = True   #if delete is true, the next line will not be saved
            else:                   #if there is no opening bracket, the line can be processed
                slash = f[line].find("/")
                if slash != -1:         #this code runs if there are multiple pos separated by a slash
                    f.insert(line+1, f[line][slash+1:])
                    f[line] = f[line][:slash]
                comma = f[line].find(",")
                if comma != -1:         #this code runs if there are multiple pos separated by a comma and space
                    f[line] = f[line].replace(",","")
                dot = f[line].find(".")
                if dot == -1 and pos:           #if there is no '.' it is a probably a new word - but it may be the pos "number", which has no '.'
                    word = f[line].replace("1","").replace("2","")
                    pos = None          #when pos, the word must have been added to the dictionary. it is safe to move onto the next.
                elif word != "":
                    pos = f[line]               #otherwise it is the pos
                    thisword = word+" "+pos
                    add_word(thisword)   #word is added to dictionary
        line = line + 1

def create_dictionary():
    global dictionary, dupli_key
    dictionary={}
    dupli_key=0
    #here True is used to signal that there is data in value[2], although the words are not irregular
    dictionary["a"] = ["article", True, "indefinite"]
    dictionary["an"] = ["article", True, "indefinite"]
    dictionary["the"] = ["article", True, "definite"]
    dictionary["she"] = ["pron", True, "they"]          #how do plural :(
    dictionary["he"] = ["pron", True, "they"]           #my wordlist had he but not she. howwwwwwww
    try:
        current_file = FILE1
        with open(FILE1+".txt","r") as file:                #opens file
            f= file.read()
            f= re.split(" |\n",f)                           #copy of file => list of lines
            f= [item.lower() for item in f]
        clean_3000(f)

        current_file = FILENAME
        with open(FILENAME+".txt","r") as file:             #opens file
            f= file.read()
            f= re.split("1|2",f)                            #copy of file => list of lines
            f= [item.lower() for item in f]
        clean_5000(f)

        current_file = FILEIRREGV
        with open(FILEIRREGV+".txt","r") as file:          #verbs
            f= file.read()
            f= re.sub(" /.+/|\n	\n","",f)
            f= f.split("\n")
            f= [item.lower() for item in f]

        current_file = WRITABLEFILE
        with open(WRITABLEFILE+".txt","w") as file:
            x= 0
            for line in f:
                if line!="":
                    file.write(line+" ")
                    x +=1
                    if x == 3:
                        file.write(":")                         #verb end eg ":read read reading :"
                        x = 0
        
        current_file = "error.."
        with open(WRITABLEFILE+".txt","r") as file:
            f= file.read()
            f= f.split(":")
            for line in f:
                wordend= line.find(" ")
                word = line[:wordend]
                if word in dictionary:
                    key= word
                    data= dictionary[key]
                    if type(data[0]) == int:
                        for i in data:
                            if dictionary[i][0] == "v":
                                data= dictionary[i]
                                key= i
                    if data[0] == "v":
                        vforms= line.split(" ")
                        while "" in vforms:
                            vforms.remove("")
                        for i in range(len(vforms)):
                            form = vforms[i]
                            slash = form.find("/")
                            if slash != -1:
                                vforms[i] = [form[:slash], form[slash+1:]]
                        data[1] = True                              #True symbolises that the word is irregular 
                        form = vforms[0]
                        if form[len(form)-1] == ",":
                            formend = form.index(",")
                            vforms[0] = form[:formend]
                            vforms.insert(1,form[formend+1:])    
                        else:
                            vforms.insert(1,form+"s")
                        data.append(vforms)
                        dictionary[key]= data
        data = dictionary["be"]
        data[1] = True                              #True symbolises that the word is irregular 
        data.append(["am","is","were","been","was","are"])   #take note! this one is super-irregular.>
        dictionary[key]= data                       #>You can check for it by looking at the length of the irregforms array>
                                                    #>or deal with it entirely separately!

        current_file = FILEIRREGN
        with open(FILEIRREGN+".txt","r") as file:            #nouns
            f= file.read()
            f= f.split("\n")
            f= [item.lower() for item in f]
            for line in f:
                wordend= line.find("\t")
                word = line[:wordend]
                if word in dictionary:
                    key= word
                    data= dictionary[key]
                    if type(data[0]) == int:
                        for i in data:
                            if dictionary[i][0] == "n":
                                data= dictionary[i]
                                key= i
                    if data[0] == "n":
                        plural= line[wordend+2:]
                        slash = plural.find(" or ")
                        if slash != -1:
                            plural= [plural[:slash], plural[slash+4:]]
                        data[1] = True                              #True symbolises that the word is irregular 
                        data.append(plural)
                        dictionary[key]= data

        current_file = FILEIRREGA
        with open(FILEIRREGA+".txt","r") as file:
            f = file.read()
            f = f.split("\n")
            f= [item.lower() for item in f]
            for i in range(0,len(f),3):
                line = f[i]
                wordend= line.find("\t")
                word = line[:wordend]
                if word in dictionary:
                    key= word
                    data= dictionary[key]
                    if type(data[0]) == int:
                        for i in data:
                            if dictionary[i][0] == "adj":
                                data= dictionary[i]
                                key= i
                    sup_comp = line[:line.find("–")].split("\t")[1:3]
                    sup_comp = [i.lower() for i in sup_comp]
                    ''' #this is not necessary with the current wordlist
                    if "/" in sup_comp[0] or "/" in sup_comp[0]:
                        sup_comp2 = []
                        sup_comp1 = []
                        for i in range(sup_comp):
                            word = sup_comp[i]
                            if "/" in word:
                                end = word.index("/")
                                sup_comp1[i] = word[:end]
                                sup_comp2.append(word[end+1:])
                            sup_comp = [sup_comp1, sup_comp2]
                            '''
                    data[1] = True                              #True symbolises that the word is irregular 
                    data.append(sup_comp)
                    dictionary[key]= data

    except:
        return f"{current_file}.txt not found"
    
    key_list = list(dictionary.keys())
    value_list = list(dictionary.values())
    pos_value = ["article","prep","adv","n","v","adj","det","pron","conj","exclam","modal","number"]
    for i in value_list:
        if i[0] not in pos_value:
            dictionary.del(key_list[value_list.index(i)])
    
    try:
        with open(DICTFILE+".json", "w") as file:      
            json.dump(dictionary, file)
    except:
        return "Error: file was not saved"

def create_database():
    try:
        connection = sqlite3.connect(DATABASENAME+".db")
        cursor = connection.cursor()
        for query in DATABASE_CREATE_QUERIES:
            cursor.execute(query)
    except sqlite3.Error as error:
        err_messg = "Failed to execute the above queries", error
        return err_messg
    finally:
        if connection:
            connection.commit()
            connection.close()


#TenseIs allows the 5 tenses taught by esol entry 3
DATABASE_CREATE_QUERIES = ("PRAGMA foreign_keys = ON;","""CREATE TABLE tblStudents (
                    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FirstName VARCHAR(30) NOT NULL,
                    LastName VARCHAR(30),
                    ContactInfo TEXT,
                    Notes TEXT
                    );""","""CREATE TABLE tblCriteria (
                    CriteriaID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TenseIs CHAR DEFAULT 0 CHECK(TenseIs IN ('PresentSimple','PresentContinuous','PastSimple','PastContinuous','FutureSimple')),
                    HasPreposition BOOLEAN DEFAULT 0,
                    HasConjunction BOOLEAN DEFAULT 0,
                    AdjectiveIs CHAR DEFAULT 0 CHECK(AdjectiveIs IN ('Positive','Superlative','Comparative'))
                    );""","""CREATE TABLE tblExercises (
                    ExerciseID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Description TEXT,
                    Date DATE DEFAULT CURRENT_DATE,
                    CriteriaID INTEGER, 
                    FOREIGN KEY (CriteriaID) 
                        REFERENCES tblCriteria(CriteriaID)
                        ON DELETE SET NULL
                    );""","""CREATE TABLE tblSentences (
                    SentenceID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Sentence VARCHAR(100) NOT NULL, 
                    CorrectedSentence VARCHAR(100), 
                    StudentID INTEGER NOT NULL,
                    ExerciseID INTEGER NOT NULL,
                    FOREIGN KEY (StudentID)
                        REFERENCES tblStudents(StudentID)
                        ON DELETE CASCADE,
                    FOREIGN KEY (ExerciseID)
                        REFERENCES tblExercises(ExerciseID)
                        ON DELETE CASCADE
                    );""","""CREATE TABLE tblErrors (
                    StudentID INTEGER NOT NULL,
                    ExerciseID INTEGER NOT NULL,
                    Spelling INTEGER DEFAULT 0,
                    SVOOrder INTEGER DEFAULT 0,
                    SVAgreement INTEGER DEFAULT 0,
                    Criteria INTEGER DEFAULT 0,
                    Articles INTEGER DEFAULT 0,
                    Prepositions INTEGER DEFAULT 0,
                    Conjunctions INTEGER DEFAULT 0,
                    PosAdjectives INTEGER DEFAULT 0,
                    Adjectives INTEGER DEFAULT 0,
                    Total INTEGER,
                    PRIMARY KEY (StudentID, ExerciseID),
                    FOREIGN KEY (StudentID)
                        REFERENCES tblStudents(StudentID)
                        ON DELETE CASCADE,
                    FOREIGN KEY (ExerciseID)
                        REFERENCES tblExercises(ExerciseID)
                        ON DELETE CASCADE
                    );""","""CREATE TRIGGER sum_errors_insert AFTER INSERT ON tblErrors
                    WHEN NEW.Total= -1
                    BEGIN
                    UPDATE tblErrors
                    SET Total = NEW.Spelling + NEW.SVOOrder + NEW.SVAgreement + NEW.Criteria + NEW.Articles + NEW.Prepositions + NEW.Conjunctions + NEW.PosAdjectives + NEW.Adjectives;
                    END;""","""CREATE TRIGGER sum_errors_update AFTER UPDATE ON tblErrors
                    WHEN NEW.total = OLD.total
                    BEGIN
                    UPDATE tblErrors
                    SET total = NEW.Spelling + NEW.SVOOrder + NEW.SVAgreement + NEW.Criteria + NEW.Articles + NEW.Prepositions + NEW.Conjunctions + NEW.PosAdjectives + NEW.Adjectives;
                    END;""")

#error = create_database()
#if error:
#    print(error)

#error = create_dictionary()
#if error:
#    print(error)
