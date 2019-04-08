#=================================#
#==TDbase GUI software============#
#==Writtten by: Simone Not========#
#==06/04/2019=====================#
#==Version: 1.3.1=================#
#=================================#

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from modules.request_handler import requestSdFile
import datetime

def windowBuild(name, geometry, background_color):
    w = Tk()
    w.title(name)
    w.geometry(geometry)
    #w.background(background_color)
    return w

def menu(window, menu_list):
    m_control = Menu(window)
    menu_arr_obj = []
    for el in menu_list:
        new_menu = Menu(m_control)
        new_menu.add_command(label="New product")
        m_control.add_cascade(label=el, menu=new_menu)
    window.config(menu=m_control)
    return menu_arr_obj

def tab(window, tabs_list):
    t_control = ttk.Notebook(window)
    tab_arr_obj = [] 
    for el in tabs_list:
        new_tab = ttk.Frame(t_control)
        t_control.add(new_tab, text=el)
        tab_arr_obj.append(new_tab)
    t_control.pack(expand=1, fill="both")
    return tab_arr_obj

def massageBox():
    return

def configureTerminal():
    return

def configLogin(window, settings_obj, settings_list, entry_width, background_color):
    
    login_arr_obj = []
    
    col = 1
    for el in settings_list:
        data_arr_obj = []
        row = 0

        name = settings_obj[el]["name"]
        content = settings_obj[el]["content"]


        lbl = Label(window, text=name)
        data_arr_obj.append(lbl) #save label obj
        lbl.grid(column=col, row=row) #add in col
        
        row += 1 #increment col

        inbox = Entry(window,width=entry_width)
        data_arr_obj.append(inbox)#save entry obj
        inbox.insert(0,content)
        inbox.grid(column=col, row=row)
        

        login_arr_obj.append(data_arr_obj) #save the obj row to the matrix
        col += 1 #increment row

    return login_arr_obj


def configEntries(window, settings_obj, settings_list, start_row, entry_width, background_color):
    
    entries_matix_oby = []

    row = start_row
    for el in settings_list:
        entry_arr_obj = []
        col = 0

        enabled = settings_obj[el]["enabled"]
        name = settings_obj[el]["name"]
        #command = json_obj[el]["command"]
        content = settings_obj[el]["content"]
        description = settings_obj[el]["description"]

        chk_state = BooleanVar()
        entry_arr_obj.append(chk_state) #save chk_state obj
        chk = Checkbutton(window, var=chk_state)
        if 1 == enabled:
            chk.select()
        chk.grid(column=col, row=row)
        col += 1 #increment col

        lbl = Label(window, text=name)
        entry_arr_obj.append(lbl) #save label obj
        lbl.grid(sticky=W, column=col, row=row) #add in col
        col += 1 #increment col

        inbox = Entry(window,width=entry_width)
        entry_arr_obj.append(inbox)#save entry obj
        inbox.insert(0,content)
        inbox.grid(column=col, row=row)
        col += 1 #increment col

        btn = Button(window, text="Set .this")
        entry_arr_obj.append(btn)#save button obj
        btn.grid(column=col, row=row)
        col += 1 #increment col

        dscrpt = Label(window, text=description)
        entry_arr_obj.append(dscrpt) #save label obj
        dscrpt.grid(sticky=W, column=col, row=row) #add in col
        col += 1 #increment col

        entries_matix_oby.append(entry_arr_obj) #save the obj row to the matrix
        row += 1 #increment row

    return entries_matix_oby

def buildScroll(window):
    txt = scrolledtext.ScrolledText(window,width=88,height=36)
    txt.grid(column=0,row=0)
    return txt

def readSingleFile(settings_obj, login_settings_list, outup_box_obj, entry_obj):
    file_name = entry_obj.get()
    request_sd_file_thread = requestSdFile(settings_obj, login_settings_list, outup_box_obj, file_name)
    request_sd_file_thread.start()
    return

def buildSdAccess(window, data_obj, entry_width, serial, settings_obj, login_settings_list):

    col = 0
    row = 1
    padding = 50
    entry_arr_obj = []

    try:
        last_file = data_obj[serial]["Last file"]
    except:
        last_file = data_obj["Data"]["First file"]

    now = datetime.datetime.now()

    txt = scrolledtext.ScrolledText(window,width=55,height=36)
    entry_arr_obj.append(txt)#save entry obj
    txt.insert(INSERT,"The stampings will be shown here.")
    txt.place(x=255, y=0)

    lbl = Label(window, text="Today file:")
    lbl.grid(sticky=W, column=col, row=row) #add in col
    col += 1 #increment col
    stamp = str(now.year)+str(now.month)+str(now.day)+".tag"
    lbl = Label(window, text=stamp)
    lbl.grid(sticky=W, column=col, row=row) #add in col
    
    row += 1
    col = 0
    lbl = Label(window, text="File Name: ", pady=padding)
    #entry_arr_obj.append(lbl) #save label obj
    lbl.grid(sticky=W, column=col, row=row) #add in col
    col += 1 #increment col

    inbox1 = Entry(window,width=entry_width)
    entry_arr_obj.append(inbox1)#save entry obj
    inbox1.insert(0,stamp)
    inbox1.grid(column=col, row=row)
    col += 1 #increment col

    btn = Button(window, text="Read", command=lambda:readSingleFile(settings_obj, login_settings_list, txt, inbox1))
    #entry_arr_obj.append(btn)#save button obj
    btn.grid(column=col, row=row)
    col += 1 #increment col
    
    row += 1
    col = 0
    lbl = Label(window, text="File Name: ")
    #entry_arr_obj.append(lbl) #save label obj
    lbl.grid(sticky=W, column=col, row=row) #add in col
    col += 1 #increment col

    inbox2 = Entry(window,width=entry_width)
    entry_arr_obj.append(inbox2)#save entry obj
    inbox2.insert(0,last_file)
    inbox2.grid(column=col, row=row)
    col += 1 #increment col

    btn = Button(window, text="Read")
    #entry_arr_obj.append(btn)#save button obj
    btn.grid(column=col, row=row)
    col += 1 #increment col

    #TITLES PLACE
    i=24
    lbl = Label(window, text="Read only the given file")
    lbl.place(x=0, y=padding+i-30)
    lbl = Label(window, text="Read al files frome the given one")
    lbl.place(x=0, y=padding*2+i-5)
    
    return entry_arr_obj

def buildInfo():
    
    return