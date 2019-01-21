#!/usr/bin/bash
. ./test_functions.sh

URL=$(build_url classify)
curl -X POST -F "image=@$1" "$URL"
