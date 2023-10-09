filename="Oxford5000"
databasename = "lengdatabase"
filename="test"                                     #test values
databasename = "mydatabase"

import re                                           #imports regex

file=open(filename+".txt","r")                      #opens file
f= file.read()
f= re.split("1|2",f)                                #copt of file => list of lines
file.close

with open(filename+".txt",'w') as file:             #clears file
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
                print(line1)
                file.write(line1)                    #saves line to file this is bad
                pos = line[x+1:]
            line = prevword + pos
        else:
            prevline = line
        print(line)
        file.write(line)                            #saves line to file

        

'''import mysql.connector
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