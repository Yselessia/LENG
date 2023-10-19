FILEDICT = "dictionary"
DATABASENAME = "lengdatabase"
DATABASENAME = "testdb"
FILEDICT = "testdictionary"
import sys
import json
import sqlite3


try:
    connection = sqlite3.connect('file:{DATABASENAME}.db?mode=rw', uri=True)
    cursor = connection.cursor()
except:
    print("Error: Unable to locate student database")
    print("Continuing with blank database")
    connection = sqlite3.connect(DATABASENAME+"_1.db")
'''
try:
    with open(FILEDICT+".json","r+") as file:
        dictionary = json.load(file)
        pass
except:
    print("Error: No dictionary. Check directory for", FILEDICT+".json")
    print("Closing program")
    sys.exit()
'''