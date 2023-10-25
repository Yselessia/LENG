FILENAME="Oxford5000"
FILEIRREGV="irregverbs"
FILEIRREGN="irregnouns"
DATABASENAME = "lengdatabase"
DICTFILE = "dictionary"
WRITABLEFILE = "temp"

#test values    <<<<<<<<<<<
DATABASENAME = "testdb"
DICTFILE = "testdictionary"

import re                                           #imports regex
import json
import sqlite3

dictionary={}
duplikey=0
def addword(line,dictionary,duplikey):
    wordend= line.find(" ")
    word= line[:wordend].replace("\n","")
    pos= line[wordend+1:].replace(".\n","")
    posdata= [pos,False]
    if word not in dictionary:
        dictionary[word] = posdata
    else:
        origvalue= dictionary[word]
        if type(origvalue[0]) == int:
            origvalue.append(duplikey)
            dictionary.update({word:origvalue})
        else:
            dictionary.update({word:[duplikey,(duplikey+1)]}) 
            dictionary[duplikey] = origvalue
            duplikey +=1
        dictionary[duplikey] = posdata
        duplikey +=1
    return duplikey

with open(FILENAME+".txt","r") as file:             #opens file
    f= file.read()
    f= re.split("1|2",f)                            #copy of file => list of lines

with open(WRITABLEFILE+".txt","w") as file:             
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
                file.write(line1)                    #saves line to file
                duplikey = addword(line1,dictionary,duplikey)
                pos = line[x+1:]
            line = prevword + pos
        else:
            prevline = line
        file.write(line)                            #saves line to file
        duplikey = addword(line,dictionary,duplikey)

with open(FILEIRREGV+".txt","r") as file:          #verbs
    f= file.read()
    f= re.sub(" /.+/|\n	\n","",f)
    f= f.split("\n")
with open(WRITABLEFILE+".txt","w") as file:
    x= 0
    for line in f:
        if line!="":
            file.write(line+" ")
            x +=1
            if x == 3:
                file.write(":")                         #verb end eg ":read read reading :"
                x = 0

with open(FILEIRREGV+".txt","r") as file:
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
                    if "v." in dictionary[i]:
                        data= dictionary[data[i]]
                        key= i
            vforms= line.split(" ")                  
            while "" in vforms:
               vforms.remove("")
            for i in range(len(vforms)):
                form = vforms[i]
                slash = form.find("/")
                if slash != -1:
                    vforms[i] = [form[:slash], form[slash+1:]]
            data[1] = True                              #True symbolises that the word is irregular 
            data.append(vforms)
            dictionary[key]= data
            
with open(FILEIRREGN+".txt","r") as file:            #nouns
    f= file.read()
    f= f.split("\n")
    for line in f:
        wordend= line.find(" 	")
        word = line[:wordend]
        if word in dictionary:
            key= word
            data= dictionary[key]
            if type(data[0]) == int:
                for i in data:
                    if "n." in dictionary[i]:
                        data= dictionary[data[i]]
                        key= i
            plural= line[wordend+2:]
            slash = plural.find(" or ")
            if slash != -1:
                plural= [plural[:slash], plural[slash+4:]]
            data[1] = True                              #True symbolises that the word is irregular 
            data.append(plural)
            dictionary[key]= data

with open(DICTFILE+".json", "w") as file:      
    json.dump(dictionary, file)

try:
    statement = 0
    connection = sqlite3.connect(DATABASENAME+".db")
    cursor = connection.cursor()
    statement =1
    cursor.execute("PRAGMA foreign_keys = ON;")
    statement =2
    cursor.execute("""CREATE TABLE tblStudents (
                StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName VARCHAR(30) NOT NULL,
                LastName VARCHAR(30),
                ContactInfo TEXT,
                Notes TEXT
                );""")
    statement =3
    cursor.execute("""CREATE TABLE tblCriteria (
                CriteriaID INTEGER PRIMARY KEY AUTOINCREMENT,
                TenseIs CHAR DEFAULT '0' CHECK(TenseIs IN ('PrS','PrC','PaS','PaC','FS')),
                HasPreposition BOOLEAN DEFAULT 0,
                HasConjunction BOOLEAN DEFAULT 0,
                HasAdjective CHAR DEFAULT '0' CHECK(HasAdjective IN ('Pos','Sup','Com'))
                );""")                          #TenseIs allows the 5 tenses taught by esol entry 3
    statement =4
    cursor.execute("""CREATE TABLE tblExercises (
                ExerciseID INTEGER PRIMARY KEY AUTOINCREMENT,
                Description TEXT,
                Date DATE DEFAULT CURRENT_DATE,
                CriteriaID INTEGER, 
                FOREIGN KEY (CriteriaID) 
                    REFERENCES tblCriteria(CriteriaID)
                    ON DELETE SET NULL
                );""")
    statement =5
    cursor.execute("""CREATE TABLE tblSentences (
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
                );""")
    statement =6
    cursor.execute("""CREATE TABLE tblErrors (
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
                );""")
    statement =7
    cursor.execute("""CREATE TRIGGER sum_errors BEFORE INSERT ON tblErrors FOR EACH ROW
                   BEGIN
                       SET NEW.Total = NEW.Spelling + NEW.SVOOrder + NEW.SVAgreement + NEW.Criteria + NEW.Articles + NEW.Prepositions + NEW.Conjunctions + NEW.PosAdjectives + NEW.Adjectives;
                   END;""")
    statement =8
    cursor.execute("""CREATE TRIGGER sum_errors_update BEFORE UPDATE ON tblErrors FOR EACH ROW
                   WHEN NEW.Total = OLD.Total
                   BEGIN
                       UPDATE tblErrors 
                       SET Total = NEW.Spelling + NEW.SVOOrder + NEW.SVAgreement + NEW.Criteria + NEW.Articles + NEW.Prepositions + NEW.Conjunctions + NEW.PosAdjectives + NEW.Adjectives
                       WHERE StudentID = NEW.StudentID AND ExerciseID = NEW.ExerciseID;
                   END;""")
except sqlite3.Error as error:
    print("Failed to execute the above queries", error, "crashed on statement", statement)
finally:
    if connection:
        connection.commit()
        connection.close()