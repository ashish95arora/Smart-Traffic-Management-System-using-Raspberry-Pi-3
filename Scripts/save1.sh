#!/bin/bash
DATE=W$(date +"%Y-%m-%d_%H%M%S")
sudo fswebcam -r 640x480 /home/pi/script/images/$DATE.jpg
/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/script/images/$DATE.jpg $DATE.jpg
