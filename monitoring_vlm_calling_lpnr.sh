#!/bin/sh
DIR="/var/lib/motion"

sudo inotifywait -m -e create --format '%w %f' "$DIR" | while read f;

do
        python3 license_plate_number_recognition.py
done