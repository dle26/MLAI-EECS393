#!/usr/local/bin/bash

export LC_CTYPE=C
args=("$@")
file=${args[0]} 
searchwords=${args[1]}
user_id=${args[2]}

#sed -E -i "" '1,100d' "$file"
sed -E -i "" 's/[ \t]*//' "$file"
sed -E -i "" '/^[[:space:]]*$/d' "$file"
awk 'length($0)>50' "$file" > "out$user_id"
#rm "$file" 
sed -E -i "" 's/[0-9]\w\+//g' "out$user_id"
sed -E -i "" 's/[]/.:;<>!=+?,"&@%()[^*]//g' "out$user_id"
sed -E -i "" 's/\\//g' "out$user_id"
awk '{print tolower($0)}' "out$user_id" > "out_2_$user_id"
sed -E -i "" '/^$/d' stop
sed -E -i "" 's/[[:space:]]*$//' stop
sed -E -i "" '/^$/d' spanishwords
sed -E -i "" 's/[[:space:]]*$//' spanishwords
sed -E -i "" '/^$/d' "$searchwords"
sed -E -i "" 's/[[:space:]]*$//' "$searchwords"
awk -f p2.awk "out_2_$user_id" > "results$user_id"
rm "out$user_id"
rm "out_2_$user_id"
sed -E -i "" 's/ //g' "results$user_id"
