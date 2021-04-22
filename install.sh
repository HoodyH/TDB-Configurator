#!/bin/bash

#install the base requirements at system level
sudo apt update
sudo apt install python3 -y 
sudo apt install python3-pip -y 

#install the main libs at system level
sudo apt install python-tk -y 

#create the virtual env
sudo apt install python3-venv -y
python3 -m venv venv
source env/bin/activate

#Install all libs required
echo Check requrements
pip3 install -r requirments 

echo Completed!
echo Run ./tdbgui.sh
