#!/usr/bin/bash
. ./helper.sh

URL=$(build_url upload)
curl -X POST -F "image=@$1" --output "test.png" "$URL"
