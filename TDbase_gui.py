#=================================#
#==TDbase GUI software============#
#==Writtten by: Simone Not========#
#==06/04/2019=====================#
#==Version: 1.3.1=================#
#=================================#

from modules.file_handler import *
from modules.request_handler import *
from modules.gui_build import *
from modules.server_handler import *

#creating the page
win_x = 900
win_y = 650
geometry = str(win_x)+"x"+str(win_y)
background_color = None
win = windowBuild("TDBASE net controller", geometry, background_color)

menu_entry = ["File", "Save", "Config"]
menu_array = menu(win, menu_entry)

tabs_entry = ["Config", "Server","Get Stampings", "File Access", "Info"]
tabs_array = tab(win, tabs_entry)

#read default settings
settings_obj = loadJsonSettings("default_calls")

#====================================================================================
#Config PAGE
#====================================================================================
login_obj = configLogin(tabs_array[0], settings_obj, login_settings_list, 13, None)
entry_obj = configEntries(tabs_array[0], settings_obj, settings_list, 2, 20, None)

full_config_thread = None #storage location for the thread
list_to_set = []

def build():
    global list_to_set
    list_to_set = []
    i = 0
    for el in login_settings_list:
        settings_obj[el]["content"] = login_obj[i][1].get()
        #print(entry_obj[i][1].get())
        i += 1
    i = 0
    for el in settings_list:
        settings_obj[el]["content"] = entry_obj[i][2].get()
        if 1 == entry_obj[i][0].get():
            list_to_set.append(settings_obj[el]["name"])
            print(settings_obj[el]["name"])
        #print(entry_obj[i][2].get())
        i += 1

def config():
    global full_config_thread
    global list_to_set
    build()
    print("calling full configuration function")
    full_config_thread = fullConfiguration(settings_obj, list_to_set, login_settings_list)
    full_config_thread.start()

def killConfig():
    global full_config_thread
    if full_config_thread != None:
        full_config_thread.join()
        full_config_thread = None
    else:
        print("The fullConfiguration thread isn't running")

#local_buttons
x_button = win_x-170
y_button = win_y-130
btn = Button(tabs_array[0], text="Confugure All", command=config)
btn.place(x=x_button, y=y_button)
y_button += 30
btn = Button(tabs_array[0], text="Abort Configuration", command=killConfig)
btn.place(x=x_button, y=y_button)

#====================================================================================
#Server PAGE
#====================================================================================

txt_sever_box = buildScroll(tabs_array[1])
txt_sever_box.insert(INSERT,"Start the server to see the meggages here.")

server_thread = None
def server():
    global server_thread
    build()
    print("calling start server function")
    server_thread = TDBaseServer(settings_obj, txt_sever_box)
    server_thread.start()

def killServer():
    global server_thread
    if server_thread != None:
        server_thread.join()
        server_thread = None
    else:
        print("The Server thread isn't running")

#local_buttons
y_button = win_y-130
btn = Button(tabs_array[1], text="Start Server", command=server)
btn.place(x=x_button, y=y_button)
y_button += 30
btn = Button(tabs_array[1], text="Stop Server", command=killServer)
btn.place(x=x_button, y=y_button)

#====================================================================================
#Server PAGE
#====================================================================================
txt_stampings_box = buildScroll(tabs_array[2])
txt_stampings_box.insert(INSERT,"The stampings will be shown here.")

get_stampings_thread = None

def getStampings():
    global get_stampings_thread
    build()
    get_stampings_thread = requestStampings(settings_obj, login_settings_list, txt_stampings_box)
    get_stampings_thread.start()
    txt_stampings_box.insert(INSERT,"\nStampings request started.")

y_button = win_y-130
btn = Button(tabs_array[2], text="Get Stampings", command=getStampings)
btn.place(x=x_button, y=y_button)
#====================================================================================
#File Access PAGE
#====================================================================================
data_obj = loadJsonData()
serial = settings_obj["Serial"]["content"]
buildSdAccess(tabs_array[3], data_obj, 12, serial, settings_obj, login_settings_list)


#====================================================================================
#Info PAGE
#====================================================================================


#====================================================================================
#Global Button QUIT
#====================================================================================

btn = Button(win, text="Quit", command=win.destroy)
btn.place(x=win_x-169, y=win_y-45)

win.mainloop()