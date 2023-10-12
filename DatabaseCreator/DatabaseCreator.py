filename="Oxford5000"
fileirregv="irregverbs"
fileirregn="irregnouns"
databasename = "lengdatabase"
filedict = ""
fileirregv="testv"                 #test values
filename="test"
fileirregn="testn"
databasename = ""

import re                                           #imports regex
import json

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

with open(filename+".txt","r") as file:             #opens file
    f= file.read()
    f= re.split("1|2",f)                            #copy of file => list of lines

with open(filename+".txt","w") as file:             
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

with open(fileirregv+".txt","r") as file:          #verbs
    f= file.read()
    f= re.sub(" /.+/|\n	\n","",f)
    f= f.split("\n")
with open(fileirregv+".txt","w") as file:
    x= 0
    for line in f:
        if line!="":
            file.write(line+" ")
            x +=1
            if x == 3:
                file.write(":")                         #verb end eg ":read read reading :"
                x = 0

with open(fileirregv+".txt","r") as file:
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
            
with open(fileirregn+".txt","r") as file:            #nouns
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

with open(filedict+".json", "w") as file:              #have not tested section
    json.dump(dictionary, file)
print(dictionary)


'''
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="SQL5964@pain"
)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE" + databasename)
mycursor.execute(#CREATE TABLE tblWords (
                 lemma VARCHAR(20) NOT NULL, 
                 partOfSpeech ENUM('noun','pronoun','verb','adverb','adjective','preposition','conjuction','interjection','article') NOT NULL,
                 irregularNoun BOOLEAN,
                 correctLemma VARCHAR(20),
                 PRIMARY KEY (lemma)
                 );
                 CREATE TABLE tblIrregPlurals (
                 irregID NOT NULL AUTO_INCREMENT, 
                 singular VARCHAR(20) NOT NULL, 
                 plural VARCHAR(20) NOT NULL, 
                 PRIMARY KEY (irregID)
                 FOREIGN KEY (singular) REFERENCES tblWords(lemma)
                 FOREIGN KEY (plural) REFERENCES tblWords(lemma)
                 );#)



#this section for testing
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x) 
mycursor.execute("DROP DATABASE databasename;")
#end testing section
'''