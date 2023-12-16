import sys
import re                                      #imports regex
import sqlite3
import customtkinter as ctk                    #imports the ctk module
from tkinter import *
from datetime import datetime
from PIL import ImageTk,Image
from matplotlib import pyplot as plt, dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import DatastoreCreator
import SentenceAnalysis

DICTFILE = "dictionary"
DATABASENAME = "langdatabase"
LOGO = "logo"
BACKICON = "backarrow"
WINDOW_ICON = "logoicon.ico"

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

def error( err_messg="Unknown Error."):
    win_err = Tk()
    win_err.overrideredirect(True)
    win_err.geometry('400x200+400+200')
    messg = Label(master= win_err, text= err_messg+"\nClosing program", font=('Arial',14))
    messg.place(relx=0.5, rely=0.5, anchor=CENTER)
    button = ctk.CTkButton(master= win_err, text="close", command=lambda: ( win_err.destroy(), sys.exit()) , fg_color='black', hover_color='black', corner_radius=10)
    button.place(relx=0.5, rely=0.9, anchor=S)
    win_err.mainloop()
def dialogue(new_messg="Dialogue error."):
    win_messg = Toplevel(root)
    win_messg.grab_set()
    win_messg.overrideredirect(True)
    win_messg.geometry('400x200+400+200')
    messg = Label(master=win_messg, text=new_messg, font=('Arial',14))
    messg.place(relx=0.5, rely=0.5, anchor=CENTER)
    button = ctk.CTkButton(master=win_messg, text="close dialogue", command=lambda: (win_messg.destroy()) , fg_color='black', hover_color='black', corner_radius=10)
    button.place(relx=0.5, rely=0.9, anchor=S)
def confirm_change(change_messg, root_tr=True):
    win_check = Toplevel(root) if root_tr == True else Tk()
    win_check.grab_set()
    confirm = BooleanVar()
    win_check.overrideredirect(True)
    win_check.geometry('400x200+400+200')
    messg = Label(master= win_check, text=change_messg, font=('Arial',16))
    messg.place(relx=0.5, rely=0.5, anchor=CENTER)
    cancel_btn = ctk.CTkButton(master= win_check, text="cancel", command=lambda: (confirm.set(False), win_check.destroy()), width=90, fg_color='black', hover_color='black', corner_radius=10)
    confirm_btn = ctk.CTkButton(master= win_check, text="confirm", command=lambda: (confirm.set(True), win_check.destroy()), width=90, fg_color='black', hover_color='black', corner_radius=10)
    cancel_btn.place(relx=0.35, rely=0.9, anchor=S)
    confirm_btn.place(relx=0.65, rely=0.9, anchor=S)
    win_check.wait_window()
    if root_tr == False:
        win_check.mainloop()
    return confirm.get()

def user_entry(prompt_messg="Enter text:"):
    win_entry = Toplevel(root)
    win_entry.grab_set()
    win_entry.overrideredirect(True)
    win_entry.geometry('400x200+400+200')
    messg = Label(master=win_entry, text=prompt_messg, font=('Arial',14))
    messg.place(relx=0.5, rely=0.2, anchor=N)
    entry_box = ctk.CTkEntry(master=win_entry, width=200, corner_radius=10, border_width=2)
    entry_box.place(relx=0.5, rely=0.6, anchor=CENTER)
    button = ctk.CTkButton(master=win_entry, text="enter", command=lambda: (win_entry.destroy()), fg_color='black', hover_color='black', corner_radius=10)
    button.place(relx=0.5, rely=0.9, anchor=S)
    win_entry.wait_window()
    user_text = entry_box.get()
    return user_text


def back_command():
    if back[0] == True:
        back[1]()
def make_commit_btn(frame, commit, messg="COMMIT", xpos=0.5):
    global commit_btn
    commit_btn = Button(frame, text=messg, command=lambda: commit(), font=('Arial', 13), height=3, width=10, borderwidth=2)
    commit_btn.place(relx=xpos, rely=0.9, anchor=S)
    return commit_btn
def set_icon(file):
    size= (70,70)
    icon = Image.open(file+'.gif')
    var = icon.resize(size)
    var = ImageTk.PhotoImage(var)
    return var
def label_box(label, ypos, frame, return_id=False):
    label_id = Label(frame, text=label.upper(), bg=bg_col2, fg='white', font=('Arial',12))
    label_id.place(relx=0.15,rely=ypos)
    if return_id==True:
        return label_id
def date_formatted(string):
    try: 
        datetime.strptime(string, '%Y-%m-%d') 
        return True
    except ValueError:
        return False
    
def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()
def new_screen(stack_prev, page_title, scroll_state=False, right_state="normal", left_state="normal", centre_state="hidden", main_state="hidden", call_true=True):
    global title, back
    back[0] = call_true
    back[1] = stack_prev
    clear_frame(right_frame)
    clear_frame(left_frame)
    clear_frame(centre_frame)
    img = icon1
    if stack_prev:
        if stack_prev != home:
            img = icon2
    back_button.configure(image=img)
    back_button.image = img
    canvas.itemconfig(main_win, state=main_state)
    canvas.itemconfig(centre_win, state=centre_state)
    canvas.itemconfig(left_win, state=left_state)
    canvas.itemconfig(right_win, state=right_state)
    try:
        scrll_id.destroy()
    except:
        pass
    
    if scroll_state == True:
        page_title = page_title.replace(" ","\n")
        xval = 288
    else:
        xval=588
    try:
        canvas.delete(title)
    except NameError:
        pass
    title = canvas.create_text(xval, 111, text=page_title, width=400, font=('Arial',25), justify=RIGHT, anchor=E)

def bg_canvas():   
    global canvas, back_button, main_win_frame, main_win, left_frame, left_win, right_frame, right_win, centre_frame, centre_win
    canvas = ResizingCanvas(root, bg=bg_col1, height = 600, width=600)
    canvas.create_arc(299, 188, 600, 288, start=10, extent=170, 
                      fill=bg_col2, outline='')
    canvas.create_rectangle(0, 230, 600, 600, fill=bg_col2, outline='')
    canvas.create_arc(0, 172, 301, 272, start=190, extent=170, 
                      fill=bg_col1, outline='')
    canvas.place(relheight=1, relwidth=1)
    back_button= Button(root, image=icon1, command=lambda:  back_command(), borderwidth=2)
    back_button.place(x=20, y=20, anchor=NW)

    main_win_frame = Frame (root, bg=bg_col2)
    main_win = canvas.create_window(300, 588, window=main_win_frame, height=300, width=300, anchor=S)
    left_frame = Frame (root, bg=bg_col2)
    left_win = canvas.create_window(22, 588, window=left_frame, height=315, width=260, anchor=SW)
    right_frame = Frame (root, bg=bg_col2)
    right_win = canvas.create_window(579, 588, window=right_frame, height=375, width=260, anchor=SE)
    centre_frame = Frame (root, bg=bg_col2)
    centre_win = canvas.create_window(300, 588, window=centre_frame, height=300, width=300, anchor=S)


def create_home():
    ex_create_btn = ctk.CTkButton(main_win_frame, text="CREATE AN EXERCISE", command=lambda: ex_create(),
                                           fg_color=bg_col1, bg_color=bg_col2, hover_color=hover_col3, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    ex_create_btn.place(relx=0.5, rely=0.11, anchor=CENTER)
    record_edit_btn = ctk.CTkButton(main_win_frame, text="EDIT STUDENT RECORDS", command=lambda: record_edit(),
                                           fg_color=bg_col1, bg_color=bg_col2, hover_color=hover_col3, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    record_edit_btn.place(relx=0.5, rely=0.35, anchor=CENTER)
    record_view_btn = ctk.CTkButton(main_win_frame, text="VIEW STUDENT RECORDS", command=lambda: record_view_choice(),
                                           fg_color=bg_col1, bg_color=bg_col2, hover_color=hover_col3, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    record_view_btn.place(relx=0.5, rely=0.59, anchor=CENTER)
    ex_view_btn = ctk.CTkButton(main_win_frame, text="VIEW EXERCISES", command=lambda: ex_view_choice(),
                                           fg_color=bg_col1, bg_color=bg_col2, hover_color=hover_col3, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    ex_view_btn.place(relx=0.5, rely=0.83, anchor=CENTER)
def home():
    new_screen(None, "NURTURING GRAMMAR MAIN MENU", False, "hidden", "hidden", "hidden", "normal", False)


def err_list_sql_format(all_errors_list,spell_error_count):
        field_names = 'Adverbs','Adjectives','Prepositions','Determiners','SVAgreement'
        fields = [i[0] for i in all_errors_list if i[0] in field_names]
        values = [i[1] for i in all_errors_list if i[0] in field_names]
        all_errors_names = [i[0] for i in all_errors_list]
        err_num = 0
        if 'verbNoSubject' in all_errors_names:
            err_num = err_num + all_errors_list[all_errors_names.index('verbNoSubject')][1]
        if 'verbRepeated' in all_errors_names:
            err_num = err_num + all_errors_list[all_errors_names.index('verbRepeated')][1]
        if 'nounRepeated' in all_errors_names:
            err_num = err_num + all_errors_list[all_errors_names.index('nounRepeated')][1]
        if err_num > 0:
            fields.append('SVOOrder')
            values.append(err_num)
        if spell_error_count > 0:
            fields.append('Spelling')
            values.append(spell_error_count)
        fields = tuple(fields)
        values = tuple(values)
        return fields, values
def err_list_readable(all_errors_names):
    readable_i = ""
    for i in all_errors_names:
        list_i = re.split(r'([A-Z])', i)
        for j in range(len(list_i)):
            if re.match(r'[A-Z]', list_i[j]):
                readable_i = " "+readable_i + list_i[j].lower()
            else:
                readable_i = readable_i + list_i[j].lower()
        readable_i = readable_i + ","
    if readable_i == "":
        readable_i = "None"
    return readable_i
def add_sentence_commit():
    id_choice = confirm_id_select()
    sentence = sentence_entry.get()
    sentence = sentence.replace('\n','')
    x = sentence.replace(' ','')
    if not (id_choice and x != ''):
        return None
    global ex_id, dictionary, all_patterns
    spell_error_count, error_sen_items = SentenceAnalysis.main_algorithm(sentence, dictionary, all_patterns, dialogue, confirm_change, crit_choice_win, user_entry)
    all_errors_list, sentence_new = SentenceAnalysis.return_values(error_sen_items[0], sentence)
    all_errors_names = [i[0] for i in all_errors_list]

    cancel_save = True
    if 'noVerbSubject' in all_errors_names:
        dialogue("Sorry, this sentence cannot be marked.\nNo verb identified.")

    else:
        index = 1
        while index < len(error_sen_items) and cancel_save == True:
            change_messg = "Corrected sentence:\n"+sentence_new
            confirm_a = confirm_change(change_messg)
            if confirm_a == True:
                readable_i = err_list_readable(all_errors_names)
                change_messg = "Errors:\n"+ readable_i
                confirm_b = confirm_change(change_messg)
            if confirm_b and confirm_b == True:
                cancel_save = False
                fields, values = err_list_sql_format(all_errors_list, spell_error_count)
                #Criteria <<<<<<<<
                if len(fields) > 0:
                    select_query = "SELECT 1 FROM tblErrors WHERE StudentID = ? AND ExerciseID = ?"
                    try:
                        cursor.execute(select_query, (id_choice, ex_id))
                        existing_record = cursor.fetchone() #Fetch one row (if any) holding "1"
                    except:
                        pass

                    if existing_record:
                        update_query = f"UPDATE tblErrors SET {', '.join(field + ' = ?' for field in fields)} WHERE StudentID = ? AND ExerciseID = ?"
                    else:
                        update_query = f"INSERT INTO tblErrors ({', '.join(fields)}, StudentID, ExerciseID) VALUES ({', '.join(['?'] * (len(fields)+2))})"
                    try:
                        cursor.execute(update_query, values+(id_choice, ex_id))
                        connection.commit()
                    except:
                        confirm = confirm_change("Error saving correction data.\nClick confirm to save the sentence anyway\nor cancel to delete sentence.")
                        if confirm == False:
                            cancel_save = True
            else:
                cancel_save = True
                all_errors_list, sentence_new = SentenceAnalysis.return_values(error_sen_items[index], sentence)
                index += 1

        if cancel_save == False:
            insert_query = "INSERT INTO tblSentences (Sentence, CorrectedSentence, StudentID, ExerciseID) VALUES (?, ?, ?, ?)"
            try:
                cursor.execute(insert_query, (sentence, sentence_new, id_choice, ex_id))
                connection.commit()
                dialogue(f"ExerciseID = {ex_id}\nStudentID = {id_choice}\nExercise saved.")
            except:
                dialogue("Error saving sentence.\n Please try again.")
        else:
            dialogue("Sentence data has been discarded.")

def add_sentence(analysis_online=True):
    if analysis_online == True:
        global sentence_entry
        new_screen(home, "CREATE EXERCISE", True)
        commit_btn = make_commit_btn(left_frame, add_sentence_commit, "SAVE")
        label_box("ENTER SENTENCE", 0.47, left_frame)
        sentence_entry = ctk.CTkEntry(left_frame, width=200, corner_radius=10, border_width = 2)
        sentence_entry.place(relx=0.25, rely=0.54)
        create_choice()
    else:
        dialogue("Sentences cannot be added at this point.\nDictionary offline")
        return None
def ex_create_commit():
    if not dictionary:
        dialogue("Cannot save exercise.\nSentence analysis unreachable")
        return None
    date = ex_date_entry.get()
    notes = descrip_entry.get(1.0,END), 
    x = notes.replace('\n','').replace(' ','')
    if '' in (date, x):
        dialogue("Please fill in all necessary fields marked *")
    elif date_formatted(date) == False:
        dialogue("Cannot save exercise.\nCheck date is valid YYYY-MM-DD")
    else:
        #makes the datetime more specific
        date_spec = datetime.now().replace(day=date).strftime('%Y-%m-%d %H:%M:%S')
        try:
            insert_query = "INSERT INTO tblExercises (Description, Date) VALUES (?, ?)"
            cursor.execute(insert_query, (notes, date_spec))
            criteria = require_entry.get()
            global ex_id
            ex_id = cursor.lastrowid
            if criteria != '':
                dialogue("The criteria feature is not available at the moment.")    # <<<<<<<<<<
                insert_query = f"INSERT INTO tblCriteria ({criteria}) VALUES (?)"
                cursor.execute(insert_query, (crit_val,))
                critId = cursor.lastrowid
                update_query = f"UPDATE tblExercises SET CriteriaID = ? WHERE ExerciseID = ?"
                cursor.execute(update_query, (critId,ex_id))
            add_sentence()
        except:
            dialogue("Error saving exercise.\n Please try again.")
def ex_create():
    global ex_date_entry, require_entry, value_entry, value_label, descrip_label, descrip_entry
    new_screen(home,"CREATE EXERCISE")
    make_commit_btn(left_frame, ex_create_commit)
    label_box("EXERCISE ID", 0.1, left_frame)
    exId_entry = ctk.CTkEntry(left_frame, width=200, corner_radius=10, border_width = 2, state='disabled', fg_color=hover_col3)
    exId_entry.place(relx=0.25, rely=0.17)
    label_box("EXERCISE DATE*", 0.31, left_frame)
    ex_date_entry = ctk.CTkEntry(left_frame, width=200, corner_radius=10, border_width = 2, font=('Arial', 14))
    ex_date_entry.insert(END, today)
    ex_date_entry.place(relx=0.25, rely=0.39)
    label_box("REQUIREMENT",0.11, right_frame)
    require_entry = ctk.CTkEntry(right_frame, width=180, corner_radius=10, border_width = 2, font=('Arial', 14), state='readonly')
    require_entry.place(relx=0.25, rely=0.17)
    add_require = Button(right_frame, text="ADD", command=lambda: crit_choice_win(), font=('Arial',10), width=5, borderwidth=2)
    add_require.place(relx=0.8, rely=0.17)

    value_label = label_box("REQUIREMENT TYPE",0.29, right_frame, True)
    value_label.place_forget()
    value_entry = ctk.CTkEntry(right_frame, width=180, corner_radius=10, border_width = 2, font=('Arial', 14))
    descrip_label = label_box("DESCRIPTION*",0.31, right_frame, True)
    descrip_entry = ctk.CTkTextbox(right_frame, width=200, height=150, corner_radius=10, border_width = 2, wrap=WORD,  font=('Arial', 14))
    descrip_entry.place(relx=0.25, rely=0.37)

def on_crit_select(event):
    global crit_val
    crit_val = 1
    selected_require = scrll_crit.get(scrll_crit.curselection())
    clear_req(True)
    require_entry.insert(0, selected_require)
    require_entry.configure(state='readonly')
    values = is_check_constraint(selected_require)
    if values:
        options.destroy()
        crit_choice_win(values, on_val_select, 0.5)
    options.destroy()
def clear_req(insert_true=False):
    require_entry.configure(state='normal')
    require_entry.delete(0, END)
    if insert_true == False:
        require_entry.configure(state='readonly')
        options.destroy()
    value_entry.place_forget()
    value_label.place_forget()
    descrip_entry.place(relx=0.25, rely=0.37)
    descrip_label.place(relx=0.15, rely=0.31)
def on_val_select(event):
    global crit_val
    crit_val = scrll_crit.get(scrll_crit.curselection())
    value_label.place(relx=0.15, rely=0.29)
    value_entry.place(relx=0.25, rely=0.35)
    value_entry.configure(state = 'normal')
    value_entry.delete(0, END)
    value_entry.insert(0, crit_val)
    value_entry.configure(state = 'readonly')
    descrip_entry.place(relx=0.25, rely=0.53)
    descrip_label.place(relx=0.15, rely=0.47)
    options.destroy()
def crit_choice_win(check_values=None, on_select=on_crit_select, btn_pos=0.65):
    global options, scrll_crit
    options = Toplevel(root)
    options.geometry("200x200+300+300")
    options.title("Exercise Requirements")
    options.grab_set()
    if not check_values:
        check_values = [row[1] for row in crit_column_info]
        Button(options, text="CANCEL", command=options.destroy).place(relx=0.35, rely=0.85)
    Button(options, text="CLEAR", command=lambda: (clear_req(), options.destroy)).place(relx=btn_pos, rely=0.85)
    scrll_crit = Listbox(options, font=('Arial', 14), relief=FLAT)
    scroller = ctk.CTkScrollbar(scrll_crit, orientation='vertical', command=scrll_crit.yview)
    scrll_crit.config(yscrollcommand=scroller.set)
    for option in check_values:
        scrll_crit.insert(END, option)
    scrll_crit.bind('<<ListboxSelect>>', on_select)
    scrll_crit.place(relx=1.0, relwidth=1, relheight=0.75, anchor=NE)
    scroller.place(relwidth=0.05, relheight=1, anchor=E)
    return options, scrll_crit
    options.mainloop()
def is_check_constraint(column_name):
    try:
        check_type_is_in = column_name.index('Is', len(column_name)-2)     #raises exception if column is not (Is) type
        select_sql_query = f"SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'tblCriteria'"
        cursor.execute(select_sql_query)
        table_definition = cursor.fetchone()[0]
        constraint_start = table_definition.index(f'CHECK({column_name} IN (') + len(f'CHECK({column_name} IN (')
        constraint_end = table_definition.index(')', constraint_start)
        accepted_values = table_definition[constraint_start:constraint_end].split(',')
        accepted_values = [value.strip().strip("'") for value in accepted_values]
        return accepted_values
    except:
        check_type_has_in = column_name.index('Has',0,3)     #returns -1 if it is NOT a boolean (Has) column
        if check_type_has_in == -1:
            dialogue("Database error.\nThis requirement is unavailable.")
            clear_req()      # <<<<<<<
        return None

def record_edit():
    new_screen(home, "EDIT RECORDS", False, "hidden", "hidden", "normal")
    stu_add_btn = ctk.CTkButton(centre_frame, text="ADD STUDENT", command=lambda: stu_add(),
                                           fg_color=bg_col1, bg_color=bg_col2, hover_color=hover_col3, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    stu_add_btn.place(relx=0.5, rely=0.11, anchor=CENTER)
    stu_edit_btn = ctk.CTkButton(centre_frame, text="EDIT RECORDS", command=lambda: stu_edit_choice(),
                                           fg_color=bg_col1, bg_color=bg_col2, hover_color=hover_col3, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    stu_edit_btn.place(relx=0.5, rely=0.35, anchor=CENTER)
    stu_remove_btn = ctk.CTkButton(centre_frame, text="REMOVE STUDENT", command=lambda: stu_remove(),
                                           fg_color=bg_col1, bg_color=bg_col2, hover_color=hover_col3, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    stu_remove_btn.place(relx=0.5, rely=0.59, anchor=CENTER)
    cancel_btn = ctk.CTkButton(centre_frame, text="CANCEL", command=lambda:  back_command(),
                                           fg_color=bg_col1, bg_color=bg_col2, hover_color=hover_col3, text_color='black', font=('Arial',20), 
                                           corner_radius=10, height=55, width=300)
    cancel_btn.place(relx=0.5, rely=0.83, anchor=CENTER)


def plot_graph(x_list, y_list, title, student="student", lbl_list=None):
    graph_win = Toplevel(root)
    graph_win.geometry('500x500')
    graph_win.title("Error-Time, "+student)
    if not lbl_list:
        lbl_list = ['spelling', 'verb order', 'subject agreement', 'criteria', 'determiners', 'prepositions', 'adjectives', 'adverbs']
    fig, ax = plt.subplots()
    for x, y, lbl in zip(x_list, y_list, lbl_list):
        ax.plot(x, y, label=lbl)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.set_xlabel('date', labelpad=10)
    ax.set_ylabel('errors per exercise')
    ax.set_title(title)
    ax.legend(loc='upper right', ncol=2)
    canvas = FigureCanvasTkAgg(fig, master=graph_win)
    canvas.draw()
    canvas.get_tk_widget().place(relheight=1, relwidth=1)
def record_view():
    def all_graph():
        plot_graph(x_list[:-1], y_list[:-1], "All errors against time", student)
    def total_graph():
        plot_graph([x_list[-1]], [y_list[-1]], "Total errors against time", student, ["all errors"])
        
    id_choice = confirm_id_select()
    if not id_choice:
        return None
    select_query = """SELECT  main.*, errors.*, exercises.Date FROM tblStudents main
    JOIN tblErrors errors ON main.StudentID = main.StudentID
    JOIN tblExercises exercises ON errors.ExerciseID = exercises.ExerciseID
    WHERE main.StudentID = ?;"""
    cursor.execute(select_query, (id_choice,))
    results = cursor.fetchall()
    y_list = [[] for _ in range(9)]
    x_list = [[] for _ in range(9)]
    for i in range(len(results)):
        for j in range(7, 16):
            y_list[j-7].append(results[i][j])
            x_list[j-7].append(datetime.strptime(results[i][-1], '%Y-%m-%d %H:%M:%S'))
    #sorting by date:
    for i in range(9):
        data = list(zip(x_list[i], y_list[i]))
        data.sort(key=lambda point: point[0])
        x_list[i], y_list[i] = zip(*data)

    #x_list, y_list, now contain 9 sublists each containing a coordinate integer or date
    student = results[0][1] +" "+ results[0][2]

    new_screen(record_view_choice, f"STUDENT {id_choice}", False)
    create_stu_view()
    make_commit_btn(right_frame, all_graph, "SEE\nALL\nERRORS", 0.33)
    make_commit_btn(right_frame, total_graph, "SEE\nOVERALL\nPROGRESS", 0.75)
    entry_widgets = [stu_id_entry, fore_name_entry, sur_name_entry, contact_entry, notes_entry]
    stu_id_entry.configure(state='normal')
    for i in range(len(entry_widgets)-1):
        entry_widgets[i].insert(END, results[0][i])
        entry_widgets[i].configure(state='readonly')
    notes_entry.insert(1.0, results[0][4])
    notes_entry.configure(height=100, state='disabled')
def record_view_choice():
    new_screen(home,"VIEW STUDENT RECORDS", True, "hidden")
    make_commit_btn(left_frame, record_view, "SELECT")
    create_choice()

def ex_view():
    id_choice = confirm_id_select('ex')
    if not id_choice:
        return None
    try:
        select_query = "SELECT * FROM tblExercises WHERE ExerciseID = ?"
        cursor.execute(select_query, (id_choice,))
        exercise_data = cursor.fetchone()
    except:
        dialogue("Database error.\nPlease try again")
    if not exercise_data:
        return None
    new_screen(ex_view_choice, f"EXERCISE {id_choice}", True, "hidden")
    label_box("EXERCISE ID", 0.05, left_frame)
    exId_entry = ctk.CTkEntry(left_frame, width=200, corner_radius=10, border_width = 2)
    exId_entry.place(relx=0.25, rely=0.14)
    exId_entry.insert(END, exercise_data[0])
    exId_entry.configure(state='readonly')
    label_box("EXERCISE DATE", 0.23, left_frame)
    ex_date_entry = ctk.CTkEntry(left_frame, width=200, corner_radius=10, border_width = 2, font=('Arial', 14))
    ex_date_entry.place(relx=0.25, rely=0.32)
    ex_date_entry.insert(END, exercise_data[2])
    ex_date_entry.configure(state='readonly')
    label_box("DESCRIPTION",0.41, left_frame, True)
    descrip_entry = ctk.CTkTextbox(left_frame, width=200, height=150, corner_radius=10, border_width = 2, wrap=WORD,  font=('Arial', 14))
    descrip_entry.place(relx=0.25, rely=0.50)
    descrip_entry.insert(1.0, exercise_data[1])
    descrip_entry.configure(state='disabled')

    create_choice("sen", id_choice)
def ex_view_choice():
    new_screen(home, "VIEW EXERCISES", True, "hidden")
    make_commit_btn(left_frame, ex_view, "SELECT")
    create_choice('ex')
    
def create_stu_view():
    global stu_id_entry, fore_name_entry, sur_name_entry, contact_entry,  notes_entry
    label_box("STUDENT ID", 0.1, left_frame)
    stu_id_entry = ctk.CTkEntry(left_frame, width=200, corner_radius=10, border_width = 2, state='disabled', fg_color=hover_col3)
    stu_id_entry.place(relx=0.25, rely=0.17)
    label_box("FORENAME(S)*", 0.31, left_frame)
    fore_name_entry = ctk.CTkEntry(left_frame, width=200, corner_radius=10, border_width = 2, font=('Arial', 14))
    fore_name_entry.place(relx=0.25, rely=0.38)
    label_box("SURNAME", 0.52, left_frame)
    sur_name_entry = ctk.CTkEntry(left_frame, width=200, corner_radius=10, border_width = 2, font=('Arial', 14))
    sur_name_entry.place(relx=0.25, rely=0.59)
    label_box("CONTACT DETAILS*",0.11, right_frame)
    contact_entry = ctk.CTkEntry(right_frame, width=200, corner_radius=10, border_width = 2,  font=('Arial', 14))
    contact_entry.place(relx=0.25, rely=0.17)
    label_box("NOTES",0.31, right_frame)
    notes_entry = ctk.CTkTextbox(right_frame, width=200, height=150, corner_radius=10, border_width = 2, wrap=WORD,  font=('Arial', 14))
    notes_entry.place(relx=0.25, rely=0.37)
def stu_add_commit():
    new_stu = (fore_name_entry.get(), contact_entry.get())
    if '' in new_stu:
        dialogue("Please fill in all necessary fields marked *")
    else:
        try:
            insert_query = "INSERT INTO tblStudents (FirstName, ContactInfo) VALUES (?, ?)"
            cursor.execute(insert_query, new_stu)
            stu_id = cursor.lastrowid
            notes =  notes_entry.get(1.0,END)
            surname = sur_name_entry.get()
            if notes != '':
                update_query = f"UPDATE tblStudents SET Notes = ? WHERE StudentID = ?"
                cursor.execute(update_query, (notes,stu_id))
            if surname != '':
                update_query = f"UPDATE tblStudents SET LastName = ? WHERE StudentID = ?"
                cursor.execute(update_query, (surname,stu_id))
            connection.commit()
            dialogue(f"StudentID = {stu_id}\nRecord saved.")
        except:
            dialogue("Error updating student records.\n Please try again.")
def stu_add():                             
    new_screen(record_edit,"ADD STUDENT RECORD")
    create_stu_view()
    make_commit_btn(left_frame, stu_add_commit)

def stu_edit_c_commit():
    id_choice = confirm_id_select()
    if not id_choice:
        return None
    select_query = f"SELECT FirstName, LastName, ContactInfo, Notes FROM tblStudents WHERE StudentID = ?"
    cursor.execute(select_query, (id_choice,))
    results = cursor.fetchone()
    stu_edit(id_choice, results)
def stu_edit_choice(): 
    new_screen(record_edit,"EDIT STUDENT RECORD", True, "hidden")                
    make_commit_btn(left_frame, stu_edit_c_commit, "SELECT")
    create_choice()

def stu_edit_commit():
    id_choice = int(stu_id_entry.get())
    new_stu = (fore_name_entry.get(), sur_name_entry.get(), contact_entry.get(), notes_entry.get(1.0, END))
    if new_stu[0] == '' or new_stu[3] =='':
        dialogue("Please fill in all necessary fields marked *")
    else:
        confirm = confirm_change("Are you sure you want to\nchange this record?")
    if confirm == True:
        try:
            update_query = f"UPDATE tblStudents SET FirstName = ?, LastName = ?, ContactInfo = ?, Notes = ?  WHERE StudentID = ?"
            cursor.execute(update_query, new_stu+(id_choice,))
            connection.commit()
            dialogue(f"StudentID = {id_choice}\nRecord updated.")
        except:
            dialogue("Error updating student records.\n Please try again.")
    else:
        dialogue("Update canceled.")
def stu_edit(id_choice, values):    
    new_screen(stu_edit_choice,"EDIT STUDENT RECORD")
    create_stu_view()
    stu_id_entry.configure(state='normal')
    stu_id_entry.insert(0, id_choice)
    stu_id_entry.configure(state='readonly')
    entry_widgets = (fore_name_entry,sur_name_entry,contact_entry, notes_entry)
    for i in range(len(entry_widgets)):
        if values[i] != None:
            try:
                entry_widgets[i].insert(0, values[i])
            except:
                entry_widgets[i].insert(1.0, values[i])
    make_commit_btn(right_frame, stu_edit_commit)

def stu_remove_commit():
    id_choice = confirm_id_select()
    if not id_choice:
        return None
    confirm = confirm_change("Are you sure you want to\ndelete this record?")
    if confirm == True:
        try:
            delete_query = "DELETE FROM tblStudents WHERE StudentID = ?"
            connection.commit(delete_query,(id_choice,))
            dialogue(f"Record for student {id_choice} deleted.")
        except:
            dialogue("Error updating student records.\n Please try again.")
    else:
        dialogue("Deletion canceled.")
def stu_remove():
    new_screen(record_edit, "DELETE STUDENT RECORD", True, "hidden")
    make_commit_btn(left_frame,  stu_remove_commit)
    create_choice()

def confirm_id_select(choose_item='stu'):
    if choose_item == 'ex':
        item = "Exercise"
    else:
        item = "Student"
    id_choice = id_entry.get()
    try:
        id_choice = int(id_choice)
        select_query = f"SELECT {item}ID FROM tbl{item}s"
        cursor.execute(select_query)
        results = cursor.fetchall()
        if (id_choice,) in results:
            return id_choice
        else:
            raise Exception
    except:
        dialogue(f"Error: The selected ID {id_choice} is invalid.")
        return None

def on_id_select(event):
    try:
        selected_id = scrll_id.get(scrll_id.curselection()).split(">")[0][1:]
        id_entry.delete(0, END)
        id_entry.insert(0, selected_id)
    except:
        pass
def create_choice(choose_item='stu', ex_id_choice=None):
    global id_entry, scrll_id
    if choose_item=='ex':
        fields = ("ExerciseID", "Date")
        column_names = [row[1] for row in crit_column_info]
        join_string = "LEFT JOIN tblCriteria c ON main.CriteriaID = c.CriteriaID"
    elif choose_item=="sen":
        fields= ("Sentence", "CorrectedSentence")
        column_names = ("FirstName","LastName")
        join_string = (f"LEFT JOIN tblStudents c ON main.StudentID = c.StudentID WHERE main.ExerciseID = {ex_id_choice}")
    else:
        fields= ("StudentID", "FirstName", "LastName")
        column_names = ("Total",)
        join_string = "LEFT JOIN tblErrors c ON main.StudentID = c.StudentID"
    if choose_item == "sen":
        label = "Sentence"
    else:
        label = fields[0][0:fields[0].find("ID")]
        label_box(f"ENTER {label} ID", 0.31, left_frame)
        id_entry = ctk.CTkEntry(left_frame, width=200, corner_radius=10, border_width = 2, font=('Arial', 14))
        id_entry.place(relx=0.25, rely=0.38)
    scrll_id = Listbox(root, bg='white', font=('Arial', 14), relief=FLAT)
    scroller = ctk.CTkScrollbar(scrll_id, orientation='vertical', command=scrll_id.yview)
    scrll_id.config(yscrollcommand=scroller.set)
    scrll_id.place(relx=1.0, relwidth=0.5, relheight=1.0, anchor=NE)
    scroller.place(relwidth=0.05, relheight=1, anchor=E)

    select_query = f"SELECT main.{', main.'.join(fields)}, c.{', c.'.join(column_names)} FROM tbl{label}s main {join_string}"
    cursor.execute(select_query)
    results = cursor.fetchall()
    if len(results) == 0:
        scrll_id.config(font=('Arial', 20))
        scrll_id.insert(0, f"NO {label.upper()}S AVAILABLE")
        id_entry.configure(state='readonly')
        commit_btn.config(state='disabled')
        return None

    results_list = []
    if choose_item == "sen":
        scrll_id.insert(END, "Sentences:\n\n")
        for row in range(len(results)):
            results_list.append(results[row][2]+" "+results[row][3]+":")
            results_list.append(results[row][0])
            results_list.append(results[row][1])
            if len(results_list) > 3:
                i = (3*row)-3
                while ":" not in results_list[i] and i >= 3:
                    i = i-1
                if results_list[i] == results_list[row*3]:
                    results_list[row*3] = ""
        results_list = [i for i in results_list if i != ""]
    else:
        scrll_id.bind('<<ListboxSelect>>', on_id_select)
        if choose_item=='stu':
            results_new = []
            for record in results:
                error_val = record[-1] if record[-1] else 0
                index = 0
                for i in range(len(results_new)):
                    error_i = results_new[i][len(record)-1] if results_new[i][len(record)-1] else 0
                    if error_val <= error_i:
                        index = i
                        break
                    else:
                        index = i + 1
                results_new.insert(index, record)
            results = results_new

        for row in range(len(results)):
            results_list.append([])
            for field in range(len(results[0])):
                if field<2:
                    results_list[row].append(str(results[row][field]))
                else:
                    if choose_item =='stu':
                        if results[row][field] != None:
                            results_list[row].append(results[row][field])     
                        break                                       #breaks after 3 items of a student's data
                    elif results[row][field] != 0 and results[row][field] == 1:
                        results_list[row].append(column_names[field-2])
                    elif results[row][field] != 0 and results[row][field]: 
                        results_list[row].append(column_names[field-2]+' '+results[row][field])
                    else:
                        break                                       #breaks if no criteria
    
    for row in results_list:
        if choose_item == "sen":
            item = row
        else:
            item = '<'+row[0]+'> '+"  ".join(row[1:])
        scrll_id.insert(END, item)


def set_connection():
    global connection,cursor
    connection = None
    try:
        connection = sqlite3.connect(f'file:{DATABASENAME}.db?mode=rw', uri=True)
        cursor = connection.cursor()
    except:
        err_messg = f"Error: Student database\n{DATABASENAME}.db not found\nClick confirm to create new database"
        confirm = confirm_change(err_messg,False)
        if confirm == True:
            sql_messg = DatastoreCreator.create_database()
            if sql_messg:
                err_messg = f"Error: Unable to create student database.\n{sql_messg}"
                error( err_messg)
            else:
                connection = sqlite3.connect(f'file:{DATABASENAME}.db?mode=rw', uri=True)
                cursor = connection.cursor()
        else:
            error(f"Error: Unable to access database.\nCheck directories for {DATABASENAME}.db")
    finally:
        if connection:
            global crit_column_info
            cursor.execute("PRAGMA table_info(tblCriteria)")
            crit_column_info = cursor.fetchall()[1:]

bg_col1 = '#e6e6e6'
bg_col2 = '#4a4a7a'
hover_col3 = '#8f8fad'
back = [True, home]
today = datetime.today().strftime('%Y-%m-%d')
set_connection()
root = Tk()
root.geometry('800x600')
root.title("Language Analysis Nurturing Grammar")
root.iconbitmap(WINDOW_ICON)
icon1 = set_icon(LOGO)
icon2 = set_icon(BACKICON)

dictionary = DatastoreCreator.set_connection_dict(confirm_change, dialogue)
all_patterns = SentenceAnalysis.compile_all_patterns()
bg_canvas()
create_home()
home()
root.mainloop()
