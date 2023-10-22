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
import customtkinter as ctk                    #imports the ctk module
from tkinter import *
from PIL import ImageTk,Image

class ResizingCanvas(Canvas):                   #*library code not mine&?
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

def error(errMessg):
    winErr = Tk()
    winErr.overrideredirect(True)
    winErr.geometry('400x200+200+200')
    messg = Label(master=winErr, text=errMessg, font=('Arial',16), height=25, width=120)
    messg.place(relx=0.5, rely=0.5, anchor=CENTER)
    button = ctk.CTkButton(master=winErr, text="close", command=winErr.destroy, fg_color='black', corner_radius=10)
    button.place(relx=0.5, rely=0.9, anchor=S)
    winErr.mainloop()

def callRootStack(x):
    x(back)
def backCommand(back):
    if back[0] == True:
        callRootStack(back[1])

def commit():
    pass
def makeCommitBtn(frame, messg="COMMIT"):
    commitBtn = Button(frame, text=messg, command=lambda: commit(), font=('Arial',12), height=3, width=8, borderwidth=2)
    commitBtn.place(relx=0.5, rely=0.99, anchor=S)

def setIcon(file):
    size= (70,70)
    icon = Image.open(file+'.gif')
    var = icon.resize(size)
    var = ImageTk.PhotoImage(var)
    return var

def clearFrame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()

def newScreen(rootStack, pageTitle, img, leftState="normal", scrollState=False, rightState="normal", centreState="hidden", mainState="hidden", callTrue=True):
    back[0] = callTrue
    back[1] = rootStack
    clearFrame(rightFrame)
    clearFrame(leftFrame)
    clearFrame(centreFrame)
    canvas.itemconfigure(title, text=pageTitle)
    backButton.configure(image=img)
    backButton.image = img
    canvas.itemconfig(mainWin, state=mainState)
    canvas.itemconfig(centreWin, state=centreState)
    canvas.itemconfig(leftWin, state=leftState)
    canvas.itemconfig(rightWin, state=rightState)
    if scrollState == False:
        rightCanvas.place_forget()
        scrollbar.place_forget()
        canvas.itemconfig(canvasSplit, state="hidden")
        canvas.coords(title, 598, 111)   #anchor is not working
    else:
        rightCanvas.place(relheight=1, relwidth=0.5, anchor=E)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
        canvas.itemconfig(canvasSplit, state="normal")
        canvas.coords(title, 298, 111)   #anchor is not working

def bgCanvas():   
    global canvas, title, backButton, mainWinFrame, mainWin, leftFrame, leftWin, rightFrame, rightWin, centreFrame, centreWin
    canvas = ResizingCanvas(root, bg=bgCol1, height = 600, width=600)
    canvas.create_arc(299, 188, 600, 288, start=10, extent=170, 
                      fill=bgCol2, outline='')
    canvas.create_rectangle(0, 230, 600, 600, fill=bgCol2, outline='')
    canvas.create_arc(0, 172, 301, 272, start=190, extent=170, 
                      fill=bgCol1, outline='')
    
    title = canvas.create_text(598, 111, text='', font=('Arial',25), justify=RIGHT, anchor=E)   #anchor is not working
    canvas.place(relheight=1, relwidth=1)
    backButton= Button(root, image=icon1, command=lambda: backCommand(back), borderwidth=2)
    backButton.place(x=20, y=20, anchor=NW)

    mainWinFrame = Frame (root, bg=bgCol2)
    mainWin = canvas.create_window(300, 588, window=mainWinFrame, height=300, width=300, anchor=S)
    leftFrame = Frame (root, bg=bgCol2)
    leftWin = canvas.create_window(22, 588, window=leftFrame, height=315, width=260, anchor=SW)
    rightFrame = Frame (root, bg=bgCol2)
    rightWin = canvas.create_window(579, 588, window=rightFrame, height=375, width=260, anchor=SE)
    centreFrame = Frame (root, bg=bgCol2)
    centreWin = canvas.create_window(300, 588, window=centreFrame, height=300, width=300, anchor=S)

def scrollCanvas():
    global rightCanvas, canvasSplit, scrollbar
    canvasSplit = canvas.create_line(300,0,300,600, width=4)
    rightCanvas = ResizingCanvas(root, bg=bgCol1, height = 600, width=300)
    rightCanvas.place(relheight=1, relwidth=0.5, anchor=E)
    scrollbar = ctk.CTkScrollbar(root, command=rightCanvas.yview)
    rightCanvas.config(yscrollcommand=scrollbar.set)
    scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor=NE)
    rightCanvas.update_idletasks()
    rightCanvas.config(scrollregion=rightCanvas.bbox(ALL))

def createHome():
    exCreateBtn = ctk.CTkButton(mainWinFrame, text="CREATE AN EXERCISE", command=lambda: exCreate(back),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    exCreateBtn.place(relx=0.5, rely=0.11, anchor=CENTER)
    recordEditBtn = ctk.CTkButton(mainWinFrame, text="EDIT STUDENT RECORDS", command=lambda: recordEdit(back),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    recordEditBtn.place(relx=0.5, rely=0.35, anchor=CENTER)
    recordViewBtn = ctk.CTkButton(mainWinFrame, text="VIEW STUDENT RECORDS", command=lambda: recordView(back),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    recordViewBtn.place(relx=0.5, rely=0.59, anchor=CENTER)
    exViewBtn = ctk.CTkButton(mainWinFrame, text="VIEW EXERCISES", command=lambda: exView(back),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    exViewBtn.place(relx=0.5, rely=0.83, anchor=CENTER)


def home(back):
    newScreen(None, "NURTURING GRAMMAR\nMAIN MENU", icon1, "hidden", False, "hidden", "hidden", "normal", False)


def exCreate(back):
    newScreen(home,"CREATE EXERCISE", icon2)
    makeCommitBtn(leftFrame)
    
def recordEdit(back):
    newScreen(home,"EDIT RECORDS", icon1, "hidden", False, "hidden", "normal")
    studentAddBtn = ctk.CTkButton(centreFrame, text="ADD STUDENT", command=lambda: studentAdd(back),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    studentAddBtn.place(relx=0.5, rely=0.11, anchor=CENTER)
    studentEditBtn = ctk.CTkButton(centreFrame, text="EDIT RECORDS", command=lambda: studentEdit(back),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    studentEditBtn.place(relx=0.5, rely=0.35, anchor=CENTER)
    studentRemoveBtn = ctk.CTkButton(centreFrame, text="REMOVE STUDENT", command=lambda: studentRemove(back),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    studentRemoveBtn.place(relx=0.5, rely=0.59, anchor=CENTER)
    cancelBtn = ctk.CTkButton(centreFrame, text="CANCEL", command=lambda: backCommand(back),
                                           fg_color=bgCol1, bg_color=bgCol2, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    cancelBtn.place(relx=0.5, rely=0.83, anchor=CENTER)

def recordView(back):
    newScreen(home,"VIEW\nSTUDENT RECORDS", icon2, "hidden", True)
    makeCommitBtn(leftFrame)
    
def exView(back):
    newScreen(home,"VIEW\nEXERCISES", icon2)

def studentAdd(back):
    newScreen(recordEdit,"ADD\nSTUDENT RECORD", icon2)
    makeCommitBtn(rightFrame)
def studentEdit(back):
    newScreen(home,"EDIT\nSTUDENT RECORD", icon2, "hidden", True)
    makeCommitBtn(leftFrame)
def studentRemove(back):
    newScreen(home,"DELETE\nSTUDENT RECORD", icon2, "hidden", True)
    makeCommitBtn(leftFrame)

'''
try:
    connection = sqlite3.connect('file:{DATABASENAME}.db?mode=rw', uri=True)
    cursor = connection.cursor()
except:
    errMessg = "Error: Unable to locate student database.\nContinuing with blank database\n"+DATABASENAME+"_1.db"
    error(errMessg)
    connection = sqlite3.connect(DATABASENAME+"_1.db")

try:
    with open(DICTFILE+".json","r+") as file:
        dictionary = json.load(file)
        pass
except:
    errMessg = "Error: No dictionary.\nCheck directory for "+DICTFILE+".json\nClosing program"
    error(errMessg)
    sys.exit()
'''

bgCol1 = '#f5f5f5'
bgCol2 = '#4a4a7a'
back = [True, home]

root = Tk()
root.geometry('800x600')
root.title("Language Analysis Nurturing Grammar")
icon1 = setIcon(LOGO)
icon2 = setIcon(BACKICON)
bgCanvas()
scrollCanvas()
createHome()
home(back) 
root.mainloop()
