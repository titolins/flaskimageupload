#!/usr/bin/bash

function build_url() {
    if [ "$ENV" == "DEBUG" ];
    then
        BASE_URL="http://localhost:5000"
    else
        BASE_URL="http://chipos.pythonanywhere.com"
    fi
    echo "$BASE_URL/$1"
}

