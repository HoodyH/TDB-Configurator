#=================================#
#==TDbase GUI software============#
#==Writtten by: Simone Not========#
#==06/04/2019=====================#
#==Version: 1.3.1=================#
#=================================#

import json

base_dir = "modules/json_file/"

settings_list = [
        "Model",
        "Serial",
        "AES key",
        "Encription",
        "MAC",
        "DHCP en",
        "IP",
        "Netmask",
        "Gateway",
        "NTP",
        "DNS",
        "TD server en",
        "TD server",
        "TD server port",
        "Daily reboot en",
        "Daily reboot h",
        "Daily reboot min",
        "Persistent ping en",
        "Persistent ping",
        "Send timeout"
    ]

login_settings_list = ["DEVICE IP","DEVICE User","DEVICE Passwd"]

tdBase_calls =   [
        [0,0, "DEVICE IP"             ,"NULL"                 ,"172.20.0.127"                           ,"Default ip in telnet for first login"],
        [0,0, "DEVICE User"           ,"NULL"                 ,"telnet"                                 ,"Default user"],
        [0,0, "DEVICE Passwd"         ,"NULL"                 ,"data"                                   ,"Default passwd"],
        [1,0, "Model"                 ,"modelkeyset"          ,"PA"						       		    ,"Set_only_secret the model" ],
        [1,0, "Serial"                ,"serialnkeyset"        ,"S061522180035"			        	    ,"Set_only_secret the serial number"],
        [1,0, "AES key"               ,"proaeskeyset"	      ,"2b7e151628aed2a6abf7158809cf4f3c"       ,"Set_only_secret the AES key"],
        [0,0, "Encription"            ,"proaesencen"          ,1                                        ,"Set_only_secret the encriprion status"],
        [0,1, "MAC"                   ,"mac"                  ,"ac:de:48:fd:0f:d0"                      ,"Set/get the MAC"],
        [0,1, "DHCP en"               ,"dhcp"	              ,1							        	,"Set/get DHCP"],  
        [0,1, "IP"                    ,"ip"                   ,"172.20.0.127"				            ,"Set/get the IP of the device"],
        [0,1, "Netmask"               ,"netmask"              ,"255.255.255.0"			                ,"Set/get netmask of the device"],
        [0,1, "Gateway"               ,"gateway"              ,"172.20.0.1"				                ,"Set/get the Gateway of the device"],
        [0,1, "NTP"                   ,"ntp+server"           ,"216.239.35.8"				            ,"Set/get NTP of the device"],
        [0,1, "DNS"                   ,"dns+server"           ,"172.20.0.201"				            ,"Set/get DNS of the device"],
        [1,0, "TD server en"          ,"tdpro"                ,1							        	,"Set/get the server abilitation"],
        [1,0, "TD server"             ,"tdpronslookup"        ,"172.20.0.132"			        	    ,"Set/get ip/domaine_name of the server"],
        [1,0, "TD server port"        ,"tdport"               ,"8080"					     	    	,"Set/get the port of the server"],
        [0,0, "Daily reboot en"       ,"reboot+schedule+en"   ,1                                        ,"Set/get the daily reboot of the server"],
        [0,0, "Daily reboot h"        ,"reboot+schedule+h"    ,23                                       ,"Set/get the hour of the reboot "],
        [0,0, "Daily reboot min"      ,"reboot+schedule+m"    ,30                                       ,"Set/get the min of the reboot"],
        [0,0, "Persistent ping en"    ,"persistent+ping+en"   ,1                                        ,"Set/get the abilitation of PING call"],
        [0,0, "Persistent ping"       ,"persistent+ping+en"   ,30                                       ,"Set/get the delay of the persistent ping"],
        [0,0, "Send timeout"          ,"send+timeout"         ,10                                       ,"Set/get the max age before send anyway"]

        
        #["Tag list"     ,"tagslist"             ,"NULL"                                 ,"Get all the stampings, sice flash"],
    ]

def createDefaultSettingsJson():

    global tdBase_calls

    data = {}

    for el in tdBase_calls:
        field = data[el[2]] = {}
        field['enabled'] = el[0]
        field['reboot_needed'] = el[1]
        field['name'] = el[2]
        field['command'] = el[3]
        field['content'] = el[4]
        field['description'] = el[5]

    json_obj = json.dumps(data, indent=4)
    file = open("modules/json_file/default_calls.json", "w")
    file.write(json_obj)
    file.close()
    return data

    #print (json_data)

def loadJsonSettings(file_name):
    global base_dir
    dir = base_dir + file_name + ".json"
    try:
        json_obj = json.loads(open(dir).read())
    except:
        try:
            json_obj = json.loads(open(base_dir + "default_calls.json").read())
        except:
            json_obj = createDefaultSettingsJson()
    
    #print(config["Model"]["content"])
    return json_obj


def createDefaultDataJson():
    data = {}
    field = data["Data"] = {}
    field["First file"] = "20190401.tag"

    json_obj = json.dumps(data, indent=4)
    file = open("modules/json_file/data.json", "w")
    file.write(json_obj)
    file.close()
    return data

def loadJsonData():
    global base_dir
    try:
        json_obj = json.loads(open(base_dir + "data.json").read())
    except:
        json_obj = createDefaultDataJson()
    return json_obj

def saveDeviceConfigurations():
    return


