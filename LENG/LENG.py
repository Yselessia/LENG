DICTFILE = "dictionary"
DATABASENAME = "lengdatabase"
LOGO = "logo"
DATABASENAME = "testdb"                 #test values
DICTFILE = "testdictionary"
LOGO = "logotest"
BACKICON = "backarrow"

import sys
import json
import sqlite3
import datetime
import customtkinter as ctk                    #imports the ctk module
from tkinter import *
from PIL import ImageTk,Image

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
    messg = Label(master=winErr, text=errMessg+"\nClosing program", font=('Arial',16), height=25, width=120)
    messg.place(relx=0.5, rely=0.5, anchor=CENTER)
    button = ctk.CTkButton(master=winErr, text="close", command=lambda: (winErr.destroy(), sys.exit()) , fg_color='black', corner_radius=10)
    button.place(relx=0.5, rely=0.9, anchor=S)
    winErr.mainloop()
def dialogue(newMessg="Dialogue error."):
    winMessg = Toplevel(root)
    winMessg.grab_set()
    winMessg.overrideredirect(True)
    winMessg.geometry('400x200+400+200')
    messg = Label(master=winMessg, text=newMessg, font=('Arial',16), height=25, width=120)
    messg.place(relx=0.5, rely=0.5, anchor=CENTER)
    button = ctk.CTkButton(master=winMessg, text="close dialogue", command=lambda: (winMessg.destroy()) , fg_color='black', corner_radius=10)
    button.place(relx=0.5, rely=0.9, anchor=S)
    winMessg.mainloop()
def confirmChange(changeMessg):
    global confirm
    confirm = False
    winCheck = Toplevel(root)
    winCheck.grab_set()
    winCheck.overrideredirect(True)
    winCheck.geometry('400x200+400+200')
    messg = Label(master=winCheck, text=changeMessg, font=('Arial',16), height=25, width=120)
    messg.place(relx=0.5, rely=0.5, anchor=CENTER)
    cancel = ctk.CTkButton(master=winCheck, text="cancel", command=lambda: (winCheck.destroy()) , fg_color='black', corner_radius=10)
    confirm = ctk.CTkButton(master=winCheck, text="confirm", command=lambda: (commit, winCheck.destroy()) , fg_color='black', corner_radius=10)
    cancel.place(relx=0.35, rely=0.9, anchor=S)
    confirm.place(relx=0.65, rely=0.9, anchor=S)
    winCheck.mainloop()
def commit():
    global confirm
    confirm = True

def backCommand():
    if back[0] == True:
        back[1]()
def makeCommitBtn(frame, commit, messg="COMMIT"):
    commitBtn = Button(frame, text=messg, command=lambda: commit(), font=('Arial',12), height=3, width=8, borderwidth=2)
    commitBtn.place(relx=0.5, rely=0.9, anchor=S)
def setIcon(file):
    size= (70,70)
    icon = Image.open(file+'.gif')
    var = icon.resize(size)
    var = ImageTk.PhotoImage(var)
    return var
def labelBox(label, ypos, frame):
    Label(frame, text=label.upper(), bg=bgCol2, fg='white', font=('Arial',12)).place(relx=0.15,rely=ypos)
def dateFormatted(string):
    try: 
        datetime.datetime.strptime(string, '%Y-%m-%d') 
        return True
    except ValueError:
        return False
    
def clearFrame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()
def newScreen(StackPrev, pageTitle, img, rightState="normal", scrollState=False, leftState="normal", centreState="hidden", mainState="hidden", callTrue=True):
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
        xVal = 288
    else:
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
    newScreen(None, "NURTURING GRAMMAR MAIN MENU", icon1, "hidden", False, "hidden", "hidden", "normal", False)

def exCreateCommit():
    newEx = (descripEntry.get(1.0,END), exDateEntry.get())
    if '' in newEx:
        dialogue("Please fill in all necessary fields marked *")
    elif dateFormatted(newEx[1]) == False:
        dialogue("Cannot save exercise.\nCheck date is valid YYYY-MM-DD")
    else:
        try:
            insertQuery = "INSERT INTO tblExercises (Description, Date) VALUES (?, ?)"
            cursor.execute(insertQuery, newEx)
            criteria = requireEntry.get()
            exId = cursor.lastrowid
            if criteria != '':
                isTrue = 1
                insertQuery = f"INSERT INTO tblCriteria ({criteria}) VALUES (?)"
                cursor.execute(insertQuery, (isTrue,))
                critId = cursor.lastrowid
                updateQuery = f"UPDATE tblExercises SET CriteriaID = '{critId}' WHERE ExerciseID = {exId}"
                cursor.execute(updateQuery)
            connection.commit()
            dialogue(f"ExerciseID = {exId}\nExercise saved.")
        except:
            dialogue("Error saving exercise.\n Please try again.")
def exCreate():
    global exDateEntry, requireEntry, descripEntry
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
    addRequire = Button(rightFrame, text="ADD", command=lambda: optionPickerWin(), font=('Arial',10), width=5, borderwidth=2)
    addRequire.place(relx=0.8, rely=0.17)
    labelBox("DESCRIPTION*",0.31, rightFrame)
    descripEntry = ctk.CTkTextbox(rightFrame, width=200, height=150, corner_radius=10, border_width = 2, wrap=WORD,  font=('Arial', 14))
    descripEntry.place(relx=0.25, rely=0.37)
def clearReq(insertTrue=False):
    requireEntry.configure(state='normal')
    requireEntry.delete(0, END)
    if insertTrue == False:
        requireEntry.configure(state='readonly')      
def onCritSelect(event):
    selectedRequire = scrllCrit.get(scrllCrit.curselection())
    clearReq(True)
    requireEntry.insert(0, selectedRequire)
    requireEntry.configure(state='readonly')
    options.destroy()
def optionPickerWin():
    global options, scrllCrit
    options = Toplevel(root)
    options.geometry("300x300+300+300")
    options.title("Exercise Requirements")
    options.grab_set()
    cursor.execute("PRAGMA table_info(tblCriteria)")
    columnInfo = cursor.fetchall()
    columnNames = [row[1] for row in columnInfo][1:]
    scrllCrit = Listbox(options, width=300, font=('Arial', 14), relief=FLAT)
    scroller = ctk.CTkScrollbar(scrllCrit, orientation='vertical', command=scrllCrit.yview)
    scrllCrit.config(yscrollcommand=scroller.set)
    for option in columnNames:
        scrllCrit.insert(END, option)
    scrllCrit.bind('<<ListboxSelect>>', onCritSelect)
    scrllCrit.place(relwidth=1, relheight=0.7, anchor=N)
    scroller.place(relwidth=0.05, relheight=1, anchor=E)
    Button(options, text="CANCEL", command=options.destroy).place(relx=0.35, rely=0.9)
    Button(options, text="CLEAR", command=lambda: (clearReq(), options.destroy)).place(relx=0.65, rely=0.9)
    options.mainloop()
#clean ui formatting ^^^^

def recordEdit():
    newScreen(home,"EDIT RECORDS", icon1, "hidden", False, "hidden", "normal")
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

def recordViewCCommit():
    valid, IDChoice = confirmIDSelect()
    if valid == True:
        recordView(IDChoice)
def recordViewChoice():
    createChoice(home,"VIEW STUDENT RECORDS")
    makeCommitBtn(leftFrame, recordViewCCommit)

def recordView():
    pass

def exViewCCommit():
    valid, IDChoice = confirmIDSelect('ex')
    if valid == True:
        exView(IDChoice)
def exViewChoice():
    createChoice(home,"VIEW EXERCISES",'ex')
    makeCommitBtn(leftFrame, exViewCCommit)

def exView():
    pass

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
def stuAdd():                               #work out *where* actually needs to be passed <3
    newScreen(recordEdit,"ADD STUDENT RECORD", icon2)
    createStuView()
    makeCommitBtn(rightFrame, stuAddCommit)

def stuEditCCommit():
    valid, IDChoice = confirmIDSelect()
    if valid == True:
        selectQuery = f"SELECT FirstName, LastName, ContactInfo, Notes FROM tblStudents WHERE StudentID = {IDChoice}"
        cursor.execute(selectQuery)
        results = cursor.fetchall()
        stuEdit(IDChoice, results)
def stuEditChoice():                 
    createChoice(recordEdit,"EDIT STUDENT RECORD")
    makeCommitBtn(leftFrame, stuEditCCommit)

def stuEditCommit():
    IDChoice = stuIdEntry.get()
    newStu = (foreNameEntry.get(), surNameEntry.get(), contactEntry.get(), notesEntry.get(1.0, END))
    if newStu[0] == '' or newStu[3] =='':
        dialogue("Please fill in all necessary fields marked *")
    else:
        confirmChange(next, "Are you sure you want to change this record?")
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
    newScreen(stuEditChoice,"EDIT STUDENT RECORD", icon2, "hidden", True)
    createStuView()
    stuIdEntry.configure(state='normal')
    stuIdEntry.insert(0, IDChoice)
    stuIdEntry.configure(state='readonly')
    foreNameEntry.insert(0, values[0])
    surNameEntry.insert(0, values[1])
    contactEntry.insert(0, values[2])
    notesEntry.insert(1.0, values[3])
    makeCommitBtn(rightFrame, stuEditCommit)

def stuRemoveCommit():
        valid, IDChoice = confirmIDSelect()
        if valid == True:
            confirmChange(next, "Are you sure you want to delete this record?")
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
    createChoice(recordEdit, "DELETE STUDENT RECORD")
    makeCommitBtn(leftFrame, stuRemoveCommit)

def confirmIDSelect(chooseItem='stu'):
        if chooseItem == 'ex':
            item = "Exercise"
        else:
            item = "Student"
        IDChoice = IDEntry.get()
        selectQuery = f"SELECT {item}ID FROM tbl{item}s"
        cursor.execute(selectQuery)
        results = cursor.fetchall()
        if IDChoice in results:
            return True, IDChoice
        else:
            dialogue(f"Error: The selected ID {IDChoice} is invalid.")
            return False, IDChoice
def onIdSelect(event):
    selectedId = scrllID.get(scrllID.curselection())
    IDEntry.delete(0, END)
    IDEntry.insert(0, selectedId)
def createChoice(StackPrev, title, chooseItem='stu'):
    global IDEntry, scrllID
    newScreen(StackPrev, title, icon2, "hidden", True)
    if chooseItem=='ex':
        fields = ("ExerciseID", "Date")
        cursor.execute("PRAGMA table_info(tblCriteria)")
        columnInfo = cursor.fetchall()
        columnNames = [row[1] for row in columnInfo][1:]
        exString = (', c.'+', c.'.join(fields)," JOIN tblCriteria c ON main.CriteriaID = c.CriteriaID")
    else:
        fields= ("StudentID", "FirstName", "LastName")
        exString = ('','')

    label = fields[0][0:fields[0].find("ID")]
    labelBox(f"ENTER {label} ID", 0.31, leftFrame)
    IDEntry = ctk.CTkEntry(leftFrame, width=200, corner_radius=10, border_width = 2, font=('Arial', 14))
    IDEntry.place(relx=0.25, rely=0.38)
    makeCommitBtn(leftFrame)                        #FIX LINE <<<<<<<<<<<<<<<<<<<<<<<<
    scrllID = Listbox(root, width=300, font=('Arial', 14), relief=FLAT)
    scroller = ctk.CTkScrollbar(scrllID, orientation='vertical', command=scrllID.yview)
    scrllID.config(yscrollcommand=scroller.set)

    selectQuery = f"SELECT main.{', main.'.join(fields)}{exString[0]} FROM tbl{label}s main{exString[1]}"
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    resultsList = []
    for row in range(len(results)):
        resultsList.append([])
        for field in range(len(results[0])):
            if field<2:
                resultsList[row].append(results[field])
            else:
                if chooseItem =='stu':
                    resultsList[row].append(results[field])     
                    break                                       #breaks after 3 items of a student's data
                elif str(results[row][field]) != '0' and results[row][field] == 1:
                    resultsList[row].append(columnNames[field-2])
                elif str(results[row][field]) != '0':
                    resultsList[row].append(columnNames[field-2]+results[row][field])
    for row in range(len(resultsList)):     
        item = ", ".join(resultsList[row])  
        scrllID.insert(END, item)

    scrllID.bind('<<ListboxSelect>>', onIdSelect)
    scrllID.place(relwidth=0.5, relheight=1)
    scroller.place(relwidth=0.05, relheight=1, anchor=E)









def setConnections():
    global connection,cursor,dictionary
    try:
        connection = sqlite3.connect(f'file:{DATABASENAME}.db?mode=rw', uri=True)
        cursor = connection.cursor()
    except:
        errMessg = f"Error: Unable to locate student database.\nCheck directory for {DATABASENAME}.db"
        error(errMessg)
    try:
        with open(DICTFILE+".json","r+") as file:
            dictionary = json.load(file)
            pass
    except:
        errMessg = f"Error: No dictionary.\nCheck directory for {DICTFILE}.json"
        error(errMessg)

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
setConnections()
bgCanvas()
createHome()
home() 
root.mainloop()
