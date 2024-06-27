#!/bin/bash

# Update package list and install Python and pip if not already installed
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Create and activate a virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install required packages
pip install -r requirements.txt

# Run the Python script
python3 your_script.py

# Deactivate the virtual environment
deactivate