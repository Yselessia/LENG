DICTFILE = "dictionary"
DATABASENAME = "lengdatabase"
LOGO = "logo"
DATABASENAME = "testdb"                 #test values
DICTFILE = "testdictionary"
LOGO = "logotest"
BACKICON = "backarrow"

import sys
import json
import re                                      #imports regex
import sqlite3
import datetime
import customtkinter as ctk                    #imports the ctk module
from tkinter import *
from PIL import ImageTk,Image
import DatabaseCreator
import SentenceAnalysis

class ResizingCanvas(Canvas):                 
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determines the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resizes the canvas 
        self.config(width=self.width, height=self.height)
        # rescales all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

def error(errMessg="Unknown Error."):
    winErr = Tk()
    winErr.overrideredirect(True)
    winErr.geometry('400x200+400+200')
    messg = Label(master=winErr, text=errMessg+"\nClosing program", font=('Arial',14), height=25, width=120)
    messg.place(relx=0.5, rely=0.5, anchor=CENTER)
    button = ctk.CTkButton(master=winErr, text="close", command=lambda: (winErr.destroy(), sys.exit()) , fg_color='black', corner_radius=10)
    button.place(relx=0.5, rely=0.9, anchor=S)
    winErr.mainloop()
def dialogue(newMessg="Dialogue error."):
    winMessg = Toplevel(root)
    winMessg.grab_set()
    winMessg.overrideredirect(True)
    winMessg.geometry('400x200+400+200')
    messg = Label(master=winMessg, text=newMessg, font=('Arial',14), height=25, width=120)
    messg.place(relx=0.5, rely=0.5, anchor=CENTER)
    button = ctk.CTkButton(master=winMessg, text="close dialogue", command=lambda: (winMessg.destroy()) , fg_color='black', corner_radius=10)
    button.place(relx=0.5, rely=0.9, anchor=S)
def confirmChange(changeMessg):
    global confirm
    confirm = False
    winCheck = Toplevel(root)
    winCheck.grab_set()
    winCheck.overrideredirect(True)
    winCheck.geometry('400x200+400+200')
    messg = Label(master=winCheck, text=changeMessg, font=('Arial',16), height=25, width=120)
    messg.place(relx=0.5, rely=0.5, anchor=CENTER)
    cancelBtn = ctk.CTkButton(master=winCheck, text="cancel", command=lambda: (winCheck.destroy()), width=90, fg_color='black', corner_radius=10)
    confirmBtn = ctk.CTkButton(master=winCheck, text="confirm", command=commit(), width=90, fg_color='black', corner_radius=10)
    cancelBtn.place(relx=0.35, rely=0.9, anchor=S)
    confirmBtn.place(relx=0.65, rely=0.9, anchor=S)
def commit():
    global confirm
    confirm = True

def backCommand():
    if back[0] == True:
        back[1]()
def makeCommitBtn(frame, commit, messg="COMMIT"):
    global commitBtn
    commitBtn = Button(frame, text=messg, command=lambda: commit(), font=('Arial',12), height=3, width=8, borderwidth=2)
    commitBtn.place(relx=0.5, rely=0.9, anchor=S)
def setIcon(file):
    size= (70,70)
    icon = Image.open(file+'.gif')
    var = icon.resize(size)
    var = ImageTk.PhotoImage(var)
    return var
def labelBox(label, ypos, frame, returnID=False):
    labelID = Label(frame, text=label.upper(), bg=bgCol2, fg='white', font=('Arial',12))
    labelID.place(relx=0.15,rely=ypos)
    if returnID==True:
        return labelID
def dateFormatted(string):
    try: 
        datetime.datetime.strptime(string, '%Y-%m-%d') 
        return True
    except ValueError:
        return False
    
def clearFrame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()
def newScreen(StackPrev, pageTitle, img, scrollState=False, rightState="normal", leftState="normal", centreState="hidden", mainState="hidden", callTrue=True):
    global title, back
    back[0] = callTrue
    back[1] = StackPrev
    clearFrame(rightFrame)
    clearFrame(leftFrame)
    clearFrame(centreFrame)
    backButton.configure(image=img)
    backButton.image = img
    canvas.itemconfig(mainWin, state=mainState)
    canvas.itemconfig(centreWin, state=centreState)
    canvas.itemconfig(leftWin, state=leftState)
    canvas.itemconfig(rightWin, state=rightState)
    if scrollState == True:
        pageTitle = pageTitle.replace(" ","\n")
        xVal = 288
    else:
        try:
            scrllID.destroy()
        except:
            pass
        xVal=588
    try:
        canvas.delete(title)
    except NameError:
        pass
    title = canvas.create_text(xVal, 111, text=pageTitle, width=400, font=('Arial',25), justify=RIGHT, anchor=E)

def bgCanvas():   
    global canvas, backButton, mainWinFrame, mainWin, leftFrame, leftWin, rightFrame, rightWin, centreFrame, centreWin
    canvas = ResizingCanvas(root, bg=bgCol1, height = 600, width=600)
    canvas.create_arc(299, 188, 600, 288, start=10, extent=170, 
                      fill=bgCol2, outline='')
    canvas.create_rectangle(0, 230, 600, 600, fill=bgCol2, outline='')
    canvas.create_arc(0, 172, 301, 272, start=190, extent=170, 
                      fill=bgCol1, outline='')
    canvas.place(relheight=1, relwidth=1)
    backButton= Button(root, image=icon1, command=lambda: backCommand(), borderwidth=2)
    backButton.place(x=20, y=20, anchor=NW)

    mainWinFrame = Frame (root, bg=bgCol2)
    mainWin = canvas.create_window(300, 588, window=mainWinFrame, height=300, width=300, anchor=S)
    leftFrame = Frame (root, bg=bgCol2)
    leftWin = canvas.create_window(22, 588, window=leftFrame, height=315, width=260, anchor=SW)
    rightFrame = Frame (root, bg=bgCol2)
    rightWin = canvas.create_window(579, 588, window=rightFrame, height=375, width=260, anchor=SE)
    centreFrame = Frame (root, bg=bgCol2)
    centreWin = canvas.create_window(300, 588, window=centreFrame, height=300, width=300, anchor=S)

def createHome():
    exCreateBtn = ctk.CTkButton(mainWinFrame, text="CREATE AN EXERCISE", command=lambda: exCreate(),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    exCreateBtn.place(relx=0.5, rely=0.11, anchor=CENTER)
    recordEditBtn = ctk.CTkButton(mainWinFrame, text="EDIT STUDENT RECORDS", command=lambda: recordEdit(),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    recordEditBtn.place(relx=0.5, rely=0.35, anchor=CENTER)
    recordViewBtn = ctk.CTkButton(mainWinFrame, text="VIEW STUDENT RECORDS", command=lambda: recordViewChoice(),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    recordViewBtn.place(relx=0.5, rely=0.59, anchor=CENTER)
    exViewBtn = ctk.CTkButton(mainWinFrame, text="VIEW EXERCISES", command=lambda: exViewChoice(),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    exViewBtn.place(relx=0.5, rely=0.83, anchor=CENTER)
def home():
    newScreen(None, "NURTURING GRAMMAR MAIN MENU", icon1, False, "hidden", "hidden", "hidden", "normal", False)

def addSentenceCommit():
    IDChoice = confirmIDSelect()
    sentence = sentenceEntry.get()
    sentence = sentence.replace('\n','')
    x = sentence.replace(' ','')
    if IDChoice and x != '':
        global exID
        x = SentenceAnalysis.clean_sentence(sentence)


            

def addSentence():
    global sentenceEntry
    newScreen(home, "CREATE EXERCISE", icon3, True)
    #makeCommitBtn(leftFrame, addSentenceCommit, "ADD NEW") <<< this should be in the top corner
    labelBox("ENTER SENTENCE", 0.45, leftFrame)
    sentenceEntry = ctk.CTkEntry(leftFrame, width=200, corner_radius=10, border_width = 2, state='disabled')
    sentenceEntry.place(relx=0.25, rely=0.52)
    createChoice()





def exCreateCommit():
    newEx = (descripEntry.get(1.0,END), exDateEntry.get())
    x = newEx[0].replace('\n','').replace(' ','')
    if '' in newEx or x=='':
        dialogue("Please fill in all necessary fields marked *")
    elif dateFormatted(newEx[1]) == False:
        dialogue("Cannot save exercise.\nCheck date is valid YYYY-MM-DD")
    else:
        try:
            insertQuery = "INSERT INTO tblExercises (Description, Date) VALUES (?, ?)"
            cursor.execute(insertQuery, newEx)
            criteria = requireEntry.get()
            global exID
            exID = cursor.lastrowid
            if criteria != '':
                dialogue("This feature is not available at the moment.")    # <<<<<<<<<<
                #insertQuery = f"INSERT INTO tblCriteria ({criteria}) VALUES (?)"
                #cursor.execute(insertQuery, (critVal,))
                #critId = cursor.lastrowid
                #updateQuery = f"UPDATE tblExercises SET CriteriaID = '{critId}' WHERE ExerciseID = {exID}"
                #cursor.execute(updateQuery)
            connection.commit()
            dialogue(f"ExerciseID = {exID}\nExercise saved.")
            addSentence()
        except:
            dialogue("Error saving exercise.\n Please try again.")
def exCreate():
    global exDateEntry, requireEntry, valueEntry, valueLabel, descripLabel, descripEntry
    newScreen(home,"CREATE EXERCISE", icon2)
    makeCommitBtn(leftFrame, exCreateCommit)
    labelBox("EXERCISE ID", 0.1, leftFrame)
    exIdEntry = ctk.CTkEntry(leftFrame, width=200, corner_radius=10, border_width = 2, state='disabled')
    exIdEntry.place(relx=0.25, rely=0.17)
    labelBox("EXERCISE DATE*", 0.31, leftFrame)
    exDateEntry = ctk.CTkEntry(leftFrame, width=200, corner_radius=10, border_width = 2, font=('Arial', 14))
    exDateEntry.insert(END, today)
    exDateEntry.place(relx=0.25, rely=0.39)
    labelBox("REQUIREMENT",0.11, rightFrame)
    requireEntry = ctk.CTkEntry(rightFrame, width=180, corner_radius=10, border_width = 2, font=('Arial', 14), state='readonly')
    requireEntry.place(relx=0.25, rely=0.17)
    addRequire = Button(rightFrame, text="ADD", command=lambda: critChoiceWin(), font=('Arial',10), width=5, borderwidth=2)
    addRequire.place(relx=0.8, rely=0.17)

    valueLabel = labelBox("REQUIREMENT TYPE",0.29, rightFrame, True)
    valueLabel.place_forget()
    valueEntry = ctk.CTkEntry(rightFrame, width=180, corner_radius=10, border_width = 2, font=('Arial', 14))
    descripLabel = labelBox("DESCRIPTION*",0.31, rightFrame, True)
    descripEntry = ctk.CTkTextbox(rightFrame, width=200, height=150, corner_radius=10, border_width = 2, wrap=WORD,  font=('Arial', 14))
    descripEntry.place(relx=0.25, rely=0.37)

def onCritSelect(event):
    global critVal
    critVal = 1
    selectedRequire = scrllCrit.get(scrllCrit.curselection())
    clearReq(True)
    requireEntry.insert(0, selectedRequire)
    requireEntry.configure(state='readonly')
    values = isCheckConstraint(selectedRequire)
    if values:
        options.destroy()
        critChoiceWin(values, onValSelect, 0.5)
    options.destroy()
def clearReq(insertTrue=False):
    requireEntry.configure(state='normal')
    requireEntry.delete(0, END)
    if insertTrue == False:
        requireEntry.configure(state='readonly')
        options.destroy()
    valueEntry.place_forget()
    valueLabel.place_forget()
    descripEntry.place(relx=0.25, rely=0.37)
    descripLabel.place(relx=0.15, rely=0.31)
def onValSelect(event):
    global critVal
    critVal = scrllCrit.get(scrllCrit.curselection())
    valueLabel.place(relx=0.15, rely=0.29)
    valueEntry.place(relx=0.25, rely=0.35)
    valueEntry.configure(state = 'normal')
    valueEntry.delete(0, END)
    valueEntry.insert(0, critVal)
    valueEntry.configure(state = 'readonly')
    descripEntry.place(relx=0.25, rely=0.53)
    descripLabel.place(relx=0.15, rely=0.47)
    options.destroy()
def critChoiceWin(checkValues=None, onSelect=onCritSelect, btnPos=0.65):
    global options, scrllCrit
    options = Toplevel(root)
    options.geometry("200x200+300+300")
    options.title("Exercise Requirements")
    options.grab_set()
    if not checkValues:
        checkValues = [row[1] for row in critColumnInfo]
        Button(options, text="CANCEL", command=options.destroy).place(relx=0.35, rely=0.85)
    Button(options, text="CLEAR", command=lambda: (clearReq(), options.destroy)).place(relx=btnPos, rely=0.85)
    scrllCrit = Listbox(options, font=('Arial', 14), relief=FLAT)
    scroller = ctk.CTkScrollbar(scrllCrit, orientation='vertical', command=scrllCrit.yview)
    scrllCrit.config(yscrollcommand=scroller.set)
    for option in checkValues:
        scrllCrit.insert(END, option)
    scrllCrit.bind('<<ListboxSelect>>', onSelect)
    scrllCrit.place(relx=1.0, relwidth=1, relheight=0.75, anchor=NE)
    scroller.place(relwidth=0.05, relheight=1, anchor=E)
    options.mainloop()
def isCheckConstraint(columnName):
    try:
        checkTypeIsIn = columnName.index('Is', len(columnName)-2)     #raises exception if column is not (Is) type
        selectSqlQuery = f"SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'tblCriteria'"
        cursor.execute(selectSqlQuery)
        tableDefinition = cursor.fetchone()[0]
        constraintStart = tableDefinition.index(f'CHECK({columnName} IN (') + len(f'CHECK({columnName} IN (')
        constraintEnd = tableDefinition.index(')', constraintStart)
        acceptedValues = tableDefinition[constraintStart:constraintEnd].split(',')
        acceptedValues = [value.strip().strip("'") for value in acceptedValues]
        return acceptedValues
    except:
        checkTypeHasIn = columnName.index('Has',0,3)     #returns -1 if it is NOT a boolean (Has) column
        if checkTypeHasIn == -1:
            dialogue("Database error.\nThis requirement is unavailable.")
            clearReq()      # <<<<<<<
        return None

def recordEdit():
    newScreen(home,"EDIT RECORDS", icon1, False, "hidden", "hidden", "normal")
    stuAddBtn = ctk.CTkButton(centreFrame, text="ADD STUDENT", command=lambda: stuAdd(),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    stuAddBtn.place(relx=0.5, rely=0.11, anchor=CENTER)
    stuEditBtn = ctk.CTkButton(centreFrame, text="EDIT RECORDS", command=lambda: stuEditChoice(),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    stuEditBtn.place(relx=0.5, rely=0.35, anchor=CENTER)
    stuRemoveBtn = ctk.CTkButton(centreFrame, text="REMOVE STUDENT", command=lambda: stuRemove(),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    stuRemoveBtn.place(relx=0.5, rely=0.59, anchor=CENTER)
    cancelBtn = ctk.CTkButton(centreFrame, text="CANCEL", command=lambda: backCommand(),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    cancelBtn.place(relx=0.5, rely=0.83, anchor=CENTER)

def recordView():
    IDChoice = confirmIDSelect()
    if IDChoice:
        pass            # <<<<<<<<<<<<<
def recordViewChoice():
    newScreen(home,"VIEW STUDENT RECORDS", icon2, True, "hidden")
    makeCommitBtn(leftFrame, recordView)
    createChoice()

def exView():
    IDChoice = confirmIDSelect('ex')
    if IDChoice:
        pass            # <<<<<<<<
def exViewChoice():
    newScreen(home,"VIEW EXERCISES", icon2, True, "hidden")
    makeCommitBtn(leftFrame, exView)
    createChoice('ex')
    
def createStuView():
    global stuIdEntry, foreNameEntry, surNameEntry, contactEntry, notesEntry
    labelBox("STUDENT ID", 0.1, leftFrame)
    stuIdEntry = ctk.CTkEntry(leftFrame, width=200, corner_radius=10, border_width = 2, state='disabled')
    stuIdEntry.place(relx=0.25, rely=0.17)
    labelBox("FORENAME(S)*", 0.31, leftFrame)
    foreNameEntry = ctk.CTkEntry(leftFrame, width=200, corner_radius=10, border_width = 2, font=('Arial', 14))
    foreNameEntry.place(relx=0.25, rely=0.38)
    labelBox("SURNAME", 0.52, leftFrame)
    surNameEntry = ctk.CTkEntry(leftFrame, width=200, corner_radius=10, border_width = 2, font=('Arial', 14))
    surNameEntry.place(relx=0.25, rely=0.59)
    labelBox("CONTACT DETAILS*",0.11, rightFrame)
    contactEntry = ctk.CTkEntry(rightFrame, width=200, corner_radius=10, border_width = 2,  font=('Arial', 14))
    contactEntry.place(relx=0.25, rely=0.17)
    labelBox("NOTES",0.31, rightFrame)
    notesEntry = ctk.CTkTextbox(rightFrame, width=200, height=150, corner_radius=10, border_width = 2, wrap=WORD,  font=('Arial', 14))
    notesEntry.place(relx=0.25, rely=0.37)
def stuAddCommit():
    newStu = (foreNameEntry.get(), contactEntry.get())
    if '' in newStu:
        dialogue("Please fill in all necessary fields marked *")
    else:
        try:
            insertQuery = "INSERT INTO tblStudents (FirstName, ContactInfo) VALUES (?, ?)"
            cursor.execute(insertQuery, newStu)
            stuId = cursor.lastrowid
            notes = notesEntry.get(1.0,END)
            surname = surNameEntry.get()
            if notes != '':
                updateQuery = f"UPDATE tblStudents SET Notes = '{notes}' WHERE StudentID = {stuId}"
                cursor.execute(updateQuery)
            if surname != '':
                updateQuery = f"UPDATE tblStudents SET LastName = '{surname}' WHERE StudentID = {stuId}"
                cursor.execute(updateQuery)
            connection.commit()
            dialogue(f"StudentID = {stuId}\nRecord saved.")
        except:
            dialogue("Error updating student records.\n Please try again.")
def stuAdd():                             
    newScreen(recordEdit,"ADD STUDENT RECORD", icon2)
    createStuView()
    makeCommitBtn(rightFrame, stuAddCommit)

def stuEditCCommit():
    IDChoice = confirmIDSelect()
    if IDChoice:
        selectQuery = f"SELECT FirstName, LastName, ContactInfo, Notes FROM tblStudents WHERE StudentID = {IDChoice}"
        cursor.execute(selectQuery)
        results = cursor.fetchall()[0]
        stuEdit(IDChoice, results)
def stuEditChoice(): 
    newScreen(recordEdit,"EDIT STUDENT RECORD", icon2, True, "hidden")                
    makeCommitBtn(leftFrame, stuEditCCommit)
    createChoice()

def stuEditCommit():
    IDChoice = int(stuIdEntry.get())
    newStu = (foreNameEntry.get(), surNameEntry.get(), contactEntry.get(), notesEntry.get(1.0, END))
    if newStu[0] == '' or newStu[3] =='':
        dialogue("Please fill in all necessary fields marked *")
    else:
        confirmChange("Are you sure you want to\nchange this record?")
        if confirm == True:
            try:
                updateQuery = f"UPDATE tblStudents SET FirstName = ?, LastName = ?, ContactInfo = ?, Notes = ?  WHERE StudentID = {IDChoice}"
                cursor.execute(updateQuery, newStu)
                connection.commit()
                dialogue(f"StudentID = {IDChoice}\nRecord updated.")
            except:
                dialogue("Error updating student records.\n Please try again.")
        else:
            dialogue("Update canceled.")
def stuEdit(IDChoice, values):    
    newScreen(stuEditChoice,"EDIT STUDENT RECORD", icon2)
    createStuView()
    stuIdEntry.configure(state='normal')
    stuIdEntry.insert(0, IDChoice)
    stuIdEntry.configure(state='readonly')
    entryWidgets = (foreNameEntry,surNameEntry,contactEntry,notesEntry)
    for i in range(len(entryWidgets)):
        if values[i] != None:
            try:
                entryWidgets[i].insert(0, values[i])
            except:
                entryWidgets[i].insert(1.0, values[i])
    makeCommitBtn(rightFrame, stuEditCommit)

def stuRemoveCommit():
    IDChoice = confirmIDSelect()
    if IDChoice:
        confirmChange("Are you sure you want to\ndelete this record?")
        if confirm == True:
            try:
                deleteQuery = "DELETE FROM tblStudents WHERE StudentID = ?"
                connection.commit(deleteQuery,(IDChoice,))
                dialogue(f"Record for student {IDChoice} deleted.")
            except:
                dialogue("Error updating student records.\n Please try again.")
        else:
            dialogue("Deletion canceled.")
def stuRemove():
    newScreen(recordEdit, "DELETE STUDENT RECORD", icon2, True, "hidden")
    makeCommitBtn(leftFrame, stuRemoveCommit)
    createChoice()

def confirmIDSelect(chooseItem='stu'):
    if chooseItem == 'ex':
        item = "Exercise"
    else:
        item = "Student"
    IDChoice = IDEntry.get()
    try:
        IDChoice = int(IDChoice)
        selectQuery = f"SELECT {item}ID FROM tbl{item}s"
        cursor.execute(selectQuery)
        results = cursor.fetchall()
        if (IDChoice,) in results:
            return IDChoice
        else:
            raise Exception
    except:
        dialogue(f"Error: The selected ID {IDChoice} is invalid.")
        return None

def onIdSelect(event):
    try:
        selectedId = scrllID.get(scrllID.curselection()).split(">")[0][1:]
        IDEntry.delete(0, END)
        IDEntry.insert(0, selectedId)
    except:
        pass
def createChoice(chooseItem='stu'):
    global IDEntry, scrllID
    if chooseItem=='ex':
        fields = ("ExerciseID", "Date")
        columnNames = [row[1] for row in critColumnInfo]
        exString = (', c.'+', c.'.join(columnNames)," LEFT JOIN tblCriteria c ON main.CriteriaID = c.CriteriaID")
    else:
        fields= ("StudentID", "FirstName", "LastName")
        exString = ('','')
    label = fields[0][0:fields[0].find("ID")]
    labelBox(f"ENTER {label} ID", 0.31, leftFrame)
    IDEntry = ctk.CTkEntry(leftFrame, width=200, corner_radius=10, border_width = 2, font=('Arial', 14))
    IDEntry.place(relx=0.25, rely=0.38)
    scrllID = Listbox(root, bg=bgCol1, font=('Arial', 14), relief=FLAT)
    scroller = ctk.CTkScrollbar(scrllID, orientation='vertical', command=scrllID.yview)
    scrllID.config(yscrollcommand=scroller.set)
    scrllID.place(relx=1.0, relwidth=0.5, relheight=1.0, anchor=NE)
    scroller.place(relwidth=0.05, relheight=1, anchor=E)

    selectQuery = f"SELECT main.{', main.'.join(fields)}{exString[0]} FROM tbl{label}s main{exString[1]}"
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    if len(results) == 0:
        scrllID.config(font=('Arial', 20))
        scrllID.insert(0, f"NO {label.upper()}S AVAILABLE")
        IDEntry.configure(state='readonly')
        commitBtn.config(state='disabled')
    else:
        scrllID.bind('<<ListboxSelect>>', onIdSelect)
        resultsList = []
        for row in range(len(results)):
            resultsList.append([])
            for field in range(len(results[0])):
                if field<2:
                    resultsList[row].append(str(results[row][field]))
                else:
                    if chooseItem =='stu':
                        if results[row][field] != None:
                            resultsList[row].append(results[row][field])     
                        break                                       #breaks after 3 items of a student's data
                    elif results[row][field] != 0 and results[row][field] == 1:
                        resultsList[row].append(columnNames[field-2])
                    elif results[row][field] != 0 and results[row][field]: 
                        resultsList[row].append(columnNames[field-2]+' '+results[row][field])
                    else:
                        break                                       #breaks if no criteria
        for row in resultsList:
            item = '<'+row[0]+'> '+"  ".join(row[1:])
            scrllID.insert(END, item)


def setConnections():
    global connection,cursor,dictionary
    try:
        connection = sqlite3.connect(f'file:{DATABASENAME}.db?mode=rw', uri=True)
        cursor = connection.cursor()
    except:
        errMessg = f"Error: Student database {DATABASENAME}.db not found\nClick confirm to create new database"
        confirmChange(errMessg)
        if confirm == True:
            sqlMessg = DatabaseCreator.create_database()
            if sqlMessg:
                errMessg = f"Error: Unable to create student database.\n{sqlMessg}"
                error(errMessg)
            else:
                connection = sqlite3.connect(f'file:{DATABASENAME}.db?mode=rw', uri=True)
                cursor = connection.cursor()
        else:
            error("Error: Unable to access database.\nCheck directories for {DATABASENAME}.db")
    finally:
        if connection:
            global critColumnInfo
            cursor.execute("PRAGMA table_info(tblCriteria)")
            critColumnInfo = cursor.fetchall()[1:]
    try:
        with open(DICTFILE+".json","r+") as file:
            dictionary = json.load(file)
            pass
    except:
        errMessg = f"Error: No dictionary {DICTFILE}.json\nClick confirm to create new database"
        confirmChange(errMessg)
        if confirm == True:
            fileMessg = DatabaseCreator.create_dictionary()
            if fileMessg:
                errMessg = f"Error: Unable to create dictionary file.\n{fileMessg}"
                error(errMessg)
        else:
            error("Error: Unable to access dictionary.\nCheck directories for {DICTFILE}.json")

bgCol1 = '#f5f5f5'
bgCol2 = '#4a4a7a'
global back
back = [True, home]
today = datetime.datetime.today().strftime('%Y-%m-%d')

root = Tk()
root.geometry('800x600')
root.title("Language Analysis Nurturing Grammar")
icon1 = setIcon(LOGO)
icon2 = setIcon(BACKICON)
icon3 = setIcon(LOGO)           # <<<<<<< this should be a unique icon 'finish'
setConnections()
bgCanvas()
createHome()
home() 
root.mainloop()
