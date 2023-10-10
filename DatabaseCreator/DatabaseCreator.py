filename="Oxford5000"
fileirregv="irregverbs"
fileirregn="irregnouns"
databasename = "lengdatabase"
fileirregv=""                 #test values
filename=""
fileirregn=""
databasename = ""

import re                                           #imports regex

def addword(word,pos,dictionary,duplikey):
    if word not in dictionary:
        dictionary[word] = pos
    else:
        origvalue= dictionary[word]
        if type(origvalue[1]) == int:
            origvalue.append(duplikey)
            dictionary.update({word:origvalue})
        else:
            dictionary.update({word:[duplikey,(duplikey+1)]}) 
            dictionary[duplikey] = origvalue
            duplikey +=1
        dictionary[duplikey] = pos
        duplikey +=1
    return duplikey

with open(filename+".txt","r") as file:             #opens file
    f= file.read()
    f= re.split("1|2",f)                            #copy of file => list of lines

with open(filename+".txt","w") as file:             #clears file
    pass

with open(filename+".txt","a") as file:             
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
                file.write(line1)                    #saves line to file this is bad
                pos = line[x+1:]
            line = prevword + pos
        else:
            prevline = line
        file.write(line)                            #saves line to file

dictionary={}
duplikey=0
with open(filename+".txt","r") as file:
    f= file.read()
    f= f.split("\n")
    for line in f:
        wordend= line.find(" ")
        word = line[:wordend]
        pos = line[wordend+1:].replace(".\n","")
        duplikey = addword(word,pos,dictionary,duplikey)

with open(fileirregv+".txt","r+") as file:          #not done - verbs -
    f= file.read()
    f= re.sub(" /.+/|\n	\n","",f)
    f= f.split("\n")
    for line in f:
        file.write(line)


with open(fileirregn+".txt","r+") as file:            #not done - nouns - 
    pass

#!! THIS SHOULD be a hash table NOT A DATABASE 

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