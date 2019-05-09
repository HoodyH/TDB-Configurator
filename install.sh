#!/bin/bash

#install the base requirements at system level
sudo apt update
sudo apt install python3
sudo apt install python3-pip

#install the main libs at system level
sudo apt install python-tk 

#create the virtual env
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate

#Install all libs required
echo Check requrements
pip3 install -r requirments 