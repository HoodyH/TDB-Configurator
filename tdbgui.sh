#!/bin/bash

#create the virtual env
source venv/bin/activate

#Install all libs required
echo Check requrements
pip3 install -r requirments 

echo Starting program
#start in a hidden terminal
#noup
python3 main.py


