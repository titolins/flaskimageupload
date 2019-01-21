#!/usr/bin/bash
. ./helper.sh

URL=$(build_url classify)
curl -X POST -F "image=@$1" "$URL"
