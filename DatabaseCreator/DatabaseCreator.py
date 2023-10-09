filename="Oxford5000"
databasename = "lengdatabase"
filename="test"                                     #test values
databasename = "mydatabase"

file=open(filename+".txt","r+")                     #opens file
f= file.read()
f.splitlines()                                      #creates copy as a list of lines

fnew = []
for i in range(len(f)):       #creates copy of list without junk data
    line = f[i-1] 
    if line.find("Oxford",1,8) == -1:
        fnew.append(line)


for line in fnew:
    line = line[:len(line)-5]+line[len(line)-2:]    #removes comprehension lvl

file.writelines(fnew)                               #saves to file
file.close

#for testing
#print file
#end testing


import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="SQL5964@pain"
)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE" + databasename)
mycursor.execute('''CREATE TABLE tblWords (
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
                 );''')





#this section for testing
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x) 
mycursor.execute("DROP DATABASE databasename;")
#end testing section