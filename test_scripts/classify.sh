#!/usr/bin/bash
echo $1

curl -X POST -F "image=@$1" http://chipos.pythonanywhere.com/classify
