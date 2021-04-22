# input_string = "PING PING0000"

# while input_string[-1] == "0":
#     input_string = input_string[:-1]
# print(input_string)

#access to the directory

import os
# os.system("cd ~/git/tdbase-fw_v2/ make program")

import subprocess

cmd = "cd ~/git/tdbase-fw_v2/ && make program"
#check_output ritorna il valore che viene stampato nel terminale
returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
print('returned value:', returned_value)

GitPython