#!/bin/bash

args=("$@")
file = ${args[0]} 

sed -i 's/[ \t]*//' file
sed -i '/^[[:space:]]*$/d' file
awk 'length($0)>50' testfile > out
rm file 
sed -i 's/[0-9]\w\+//g' out
sed -i 's/[]/.:;<>!=+?,"&@%()[^*]//g' out
sed -i 's/\\//g' out
sed -i 's/[A-Z]/\L&/g' out
sed -i '/^$/d' stop
sed -i 's/[[:space:]]*$//' stop
sed -i '/^$/d' spanishwords
sed -i 's/[[:space:]]*$//' spanishwords
awk -v topic=$word -f p2.awk out > "results$user_id"
rm out
sed -i 's/ //g' "results$user_id"
