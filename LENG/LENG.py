import mysql.connector

try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SQL5964@pain"
    database="lengdatabase"
    )

    mycursor = mydb.cursor()
except:
    print("Error: Database does not exist")
