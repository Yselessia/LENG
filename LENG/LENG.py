DICTFILE = "dictionary"
DATABASENAME = "lengdatabase"
DATABASENAME = "testdb"                 #test values
DICTFILE = "testdictionary"
import sys
import json
import sqlite3
import time
import tkinter
import customtkinter                    #imports the CustomTkinter module
from tkinter import *
bgCol1 = '#f5f5f5'
bgCol2 = '#4a4a7a'

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
    window = Canvas(winErr, bg=('black'))
    window.pack(expand=1, fill=BOTH)
    label = Label(master=winErr, width=120, height=25, text=errMessg, font=16)  #font=16 incorrect syntax
    label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    button = customtkinter.CTkButton(master=winErr, fg_color='black', text="close", corner_radius=10, command=winErr.destroy)
    button.place(relx=0.5, rely=0.9, anchor=tkinter.S)
    winErr.mainloop()

def bgCanvas():
    c = ResizingCanvas(root, bg=bgCol1, height = '600',width=600)
    c.create_arc(299, 188, 600, 288, start=10, extent=170, 
                fill=bgCol2, outline='')
    c.create_rectangle(0, 230, 600, 600, fill=bgCol2, outline='')
    c.create_arc(0, 172, 301, 272, start=190, extent=170, 
                fill=bgCol1, outline='')
    c.pack(fill='both', expand=True)
    return c


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

def home(canvas):
    title = Label(master=root, text="NURTURING GRAMMAR\nMAIN MENU", bg=bgCol1, fg='black', font=40, justify=RIGHT)  #font=40 incorrect syntax
    canvas.create_window(600, 111, window=title, anchor=tkinter.E)



root = Tk()
root.geometry('800x600')
root.title("Language Analysis Nurturing Grammar")
c = bgCanvas()
home(c)  

root.mainloop()
