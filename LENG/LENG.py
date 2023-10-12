FILEDICT = "dictionary"             #LOAD FROM APPROPRIATE FOLDER!!

import json
import mysql.connector

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SQL5964@pain"     #is this correct???
        database="lengdatabase"
    )

    mycursor = mydb.cursor()
except:
    print("Error: Unable to access student database")

try:
    with open(FILEDICT,".json","r+") as file:
        dictionary = json.load(file)
        pass
except:
    print("Error: No dictionary. Check directory for", FILEDICT+".json")