#!/usr/local/bin/bash

args=("$@")
url=${args[0]} 
user_id=${args[1]}

/usr/local/bin/lynx --dump --nolist "$url" > "html_text$user_id"
