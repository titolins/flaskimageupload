#!/usr/bin/bash
. ./test_functions.sh

URL=$(build_url upload)
curl -X POST -F "image=@$1" --output "test.png" "$URL"
