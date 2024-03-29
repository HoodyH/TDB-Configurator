#=================================#
#==TDbase GUI software============#
#==Writtten by: Simone Not========#
#==06/04/2019=====================#
#==Version: 1.3.1=================#
#=================================#

import threading
import requests
from time import sleep
from tkinter import *
import subprocess 

timeout_connection = 5
timeout_short_request = 3
timeout_long_request = 10


device_config_thread_lock = 0

class deviceConfiguration(threading.Thread):
        def __init__(self, settings_obj, list_to_set, login_settings_list):
                self._stopevent = threading.Event(  )
                self._sleepperiod = 1.0
                super(deviceConfiguration, self).__init__()
                self.settings_obj = settings_obj
                self.list_to_set = list_to_set
                self.login_settings_list = login_settings_list

        def join(self, timeout=None):
                #Force stop of the thread.
                self._stopevent.set()
                threading.Thread.join(self, timeout)

        def run(self):
                global timeout_connection
                global timeout_short_request
                global device_config_thread_lock
                if 1 == device_config_thread_lock:
                        print("There is alread an ongoing config routine!")
                        return
                device_config_thread_lock = 1
                ip_device = self.settings_obj[self.login_settings_list[0]]["content"]
                user = self.settings_obj[self.login_settings_list[1]]["content"]
                passwd = self.settings_obj[self.login_settings_list[2]]["content"]

                reboot = 0

                for el in self.list_to_set:
                        if self._stopevent.isSet():
                                device_config_thread_lock = 0
                                print("\nUSER ABORT!")
                                return

                        name = self.settings_obj[el]["name"]
                        content = self.settings_obj[el]["content"]
                        command = self.settings_obj[el]["command"]
                        reboot_needed = self.settings_obj[el]["reboot_needed"]
                        
                        if 1 == reboot_needed:
                             reboot = 1
                           
                        print("{}: {}".format(name, content))
                        try:
                                requests.get("http://{}/ecmd?{}+{}".format(ip_device, command, content), auth=(user, passwd) ,timeout=(timeout_connection, timeout_short_request))
                        except:
                                print("I can't comunicate with the Decive")
                                device_config_thread_lock = 0
                                return
                        sleep(0.2)
                
                if 1 == reboot:
                        try:
                                requests.get("http://"+ip_device+"/ecmd?reset", auth=(user, passwd) ,timeout=(timeout_connection, timeout_short_request))
                                print("\nRebooting!\nDone")
                        except:
                                print("I can't reboot the Decive")
                                device_config_thread_lock = 0
                                return
                else:
                        print("\nDONE!")
                device_config_thread_lock = 0


request_stampings_thread_lock = 0

class requestStampings(threading.Thread):
        def __init__(self, settings_obj, login_settings_list, outup_box_obj):
                super(requestStampings, self).__init__()
                self.settings_obj = settings_obj
                self.login_settings_list = login_settings_list
                self.outup_box_obj = outup_box_obj

        def run(self):
                global timeout_connection
                global timeout_long_request
                global request_stampings_thread_lock
                if 1 == request_stampings_thread_lock:
                        print("The request has already begin!")
                        return
                request_stampings_thread_lock = 1
                ip_device = self.settings_obj[self.login_settings_list[0]]["content"]
                user = self.settings_obj[self.login_settings_list[1]]["content"]
                passwd = self.settings_obj[self.login_settings_list[2]]["content"]

                content = ""
                command = "tagslist"
                try:
                        out = requests.get("http://{}/ecmd?{}+{}".format(ip_device, command, content), auth=(user, passwd) ,timeout=(timeout_connection, timeout_long_request))
                except:
                        print("I can't comunicate with the Decive")
                        request_stampings_thread_lock = 0
                        return
                self.outup_box_obj.insert(INSERT, "\n\n")
                self.outup_box_obj.insert(INSERT, out.text)
                print("\nNo reboot needed\nDONE!")
                request_stampings_thread_lock = 0


request_sd_file_thread_lock = 0

class requestSdFile(threading.Thread):
        def __init__(self, settings_obj, login_settings_list, outup_box_obj, file_name):
                super(requestSdFile, self).__init__()
                self.settings_obj = settings_obj
                self.login_settings_list = login_settings_list
                self.outup_box_obj = outup_box_obj
                self.file_name = file_name

        def run(self):
                global timeout_connection
                global timeout_long_request
                global request_sd_file_thread_lock
                if 1 == request_sd_file_thread_lock:
                        print("The request has already begin!")
                        return
                request_sd_file_thread_lock = 1
                ip_device = self.settings_obj[self.login_settings_list[0]]["content"]
                user = self.settings_obj[self.login_settings_list[1]]["content"]
                passwd = self.settings_obj[self.login_settings_list[2]]["content"]

                try:
                        out = requests.get("http://{}/{}".format(ip_device, self.file_name), auth=(user, passwd) ,timeout=(timeout_connection, timeout_long_request))
                except:
                        print("I can't comunicate with the Decive")
                        request_sd_file_thread_lock = 0
                        return
                
                self.outup_box_obj.insert(INSERT, "\n\n")     
                self.outup_box_obj.insert(INSERT, out.text)
                if out.text != "File Not Found":
                        self.outup_box_obj.insert(INSERT, "Stampings form: "+ self.file_name + "\n")  
                        i = 0
                        for x in out.text:
                                if x == "\n":
                                        i += 1
                        self.outup_box_obj.insert(INSERT, "There are "+ str(i) + " stampings in this file\n")  

                print("\nDONE!")
                request_sd_file_thread_lock = 0



def ping():
        for ping in range(239,241): 
                address = "10.32.10." + str(ping) 
                res = subprocess.call(['ping', '-c', '3', address]) 
                if res == 0: 
                        print( "ping to", address, "OK") 
                elif res == 2: 
                        print("no response from", address) 
                else: 
                        print("ping to", address, "failed!") 


from socket import *
import time

def hostFind():
        target = input('Enter the host to be scanned: ')
        t_IP = gethostbyname(target)
        startTime = time.time()
        print ('Starting scan on host: ', t_IP)
   
        for i in range(50, 500):
                s = socket(AF_INET, SOCK_STREAM)
                
                conn = s.connect_ex((t_IP, i))
                if(conn == 0) :
                        print ('Port %d: OPEN' % (i,))
                s.close()
        print('Time taken:', time.time() - startTime)

