import socket 
  
# Function to display hostname and 
# IP address 
def getHostNameIP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname("tdbase") 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
    except: 
        print("Unable to get Hostname and IP") 
  
getHostNameIP()
