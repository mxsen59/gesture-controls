#!/bin/bash

echo "INSTALLING DEPENDENCIES..."
sudo apt-get install python3-opencv -y
pip install pyalsaaudio
pip install pynput
pip install autopy
echo "FINISHED INSTALLING DEPENDENCIES."