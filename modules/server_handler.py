#=================================#
#==TDbase GUI software============#
#==Writtten by: Simone Not========#
#==06/04/2019=====================#
#==Version: 1.3.1=================#
#=================================#

import socketserver
import socket
from Crypto.Cipher import AES
import threading
from tkinter import *
import datetime

HEADER_DIM = 133
#2b7e151628aed2a6abf7158809cf4f3c
default_passphrase_256 = "2b7e151628aed2a6ab22158809cf4f3c"
default_passphrase_128 = "2b7e151628aed2a6"

def getTime(now):
    return "On {}/{}/{} at {}:{}:{}".format(str(now.day), str(now.month), str(now.year), str(now.hour), str(now.minute), str(now.second))

class printClass:
    def __init__(self, outup_box_obj):
            self.outup_box_obj = outup_box_obj
    
    def setOutputBox(self, outup_box_obj):
        self.outup_box_obj = outup_box_obj

    def printClear(self, data, client):
        now = datetime.datetime.now()
        self.outup_box_obj.insert(INSERT, "Receved data in clear from {}\n{}\n".format(client, getTime(now)))
        self.outup_box_obj.insert(INSERT, "{}\n\n".format(data))
    
    def printEncripted(self, data, client):
        now = datetime.datetime.now()
        self.outup_box_obj.insert(INSERT, "Receved Encripted data from {}\n{}\n".format(client, getTime(now)))
        self.outup_box_obj.insert(INSERT, "{}\n\n".format(data))

class ECBClass:
    def __init__(self, key):
            self.key = key
    
    def setKey(self, key):
        self.key = key

    def decript(self, encrypted):
        aes = AES.new(self.key, AES.MODE_ECB)
        return aes.decrypt(encrypted)


print_s = printClass(None)
ecb = ECBClass(default_passphrase_128)


def stampings_formatting(input_string):
    out_string = ''

    if input_string.find('"') == 0:
        input_string = input_string[1:]
    else:
        # clean the message from the 0
        # print("no_stampings")
        while input_string[-1] == "0":
            input_string = input_string[:-1]
        return input_string

    while True:
        pos = input_string.find('"')
        if pos == -1:
            break
        out_string += '"' + input_string[:pos+1] + "\n"
        input_string = input_string[pos+2:]
    
    return out_string


class TDBaseHandler(socketserver.StreamRequestHandler):

    def handle(self):
        global HEADER_DIM
        global print_s
        global ecb
        
        #print("Incoming Connection TDBase <{}>".format(self.client_address[0]))
        self.request.settimeout(20)
        self.data = self.request.recv(512+HEADER_DIM) #new header dimension
        print(self.data)
        print()
        if self.data:
            _data = self.data.decode('Latin1').split('\r\n\r\n')[1].encode('Latin1')
        else:
            return

        try:
            _data = _data.decode("utf-8").strip()

            print_s.printClear(stampings_formatting(_data), self.client_address[0])
        except Exception as exc:
            _data = ecb.decript(_data).decode("utf-8").strip()
            print_s.printEncripted(stampings_formatting(_data), self.client_address[0])
        finally:
            self.wfile.write("hello".encode("utf-8"))
        #print("Connection ended")

td_base_server_thread_lock = 0

class TDBaseServer(threading.Thread):
        def __init__(self, settings_obj, outup_box_obj):
                super(TDBaseServer, self).__init__()
                self.settings_obj = settings_obj
                self.outup_box_obj = outup_box_obj

        def run(self):
                global td_base_server_thread_lock
                global print_s
                global ecb

                if 1 == td_base_server_thread_lock:
                        print("The request has already begin!")
                        return
                td_base_server_thread_lock = 1

                server_en = self.settings_obj["TD server en"]["content"]
                server_ip = self.settings_obj["TD server"]["content"]
                server_port = self.settings_obj["TD server port"]["content"]
                key = self.settings_obj["AES key"]["content"]
                
                ecb.setKey(key)
                print_s.setOutputBox(self.outup_box_obj)

                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                device_ip = s.getsockname()[0]
                s.close()
                
                self.outup_box_obj.insert(INSERT, "\n\n")

                if not int(server_en) == 1:
                    self.outup_box_obj.insert(INSERT, "WARNING: SERVER on the device is DISABLED [{}]\n".format(server_en))
                
                if not str(device_ip) == str(server_ip):
                    self.outup_box_obj.insert(INSERT, "WARNING: SERVER IP on device could be setted wrong [{}]\n".format(server_ip))

                self.outup_box_obj.insert(INSERT, "Starting server on {}:{}\n\n".format(device_ip, server_port))
                
                socketserver.ThreadingTCPServer.allow_reuse_address = True
                server = socketserver.ThreadingTCPServer(('0', int(server_port)), TDBaseHandler)
                print("Avvio ServerTEST per TDBase")
                try:
                    server.serve_forever()
                except KeyboardInterrupt:
                    server.shutdown()
                    server.socket.close()
                    print("Terminazione server")
                    self.outup_box_obj.insert(INSERT, "Shuting down\n")
                td_base_server_thread_lock = 0
