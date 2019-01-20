#!/usr/bin/bash
echo $1

curl -X POST -F "image=@titu.jpg" http://chipos.pythonanywhere.com/classify
