#!/usr/bin/bash
echo $1

curl -X POST -F "image=@$1" --output "test.png" http://chipos.pythonanywhere.com/upload
