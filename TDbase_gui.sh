#!/bin/bash

source venv/bin/activate

#Install all libs required
echo Check requrements
pip install -r requirments 

echo Starting program
#start in a hidden terminal
#noup
python3 TDbase_gui.py


