#!/bin/bash

args=("$@")
word=${args[0]} 
year1=${args[1]}  
year2=${args[2]}  
paper=${args[3]}  
related=${args[4]}  
user_id=${args[5]}  

none="None"
numyears=$((year2-year1))
k=0

for ((i=0; i<=$numyears;i++))
do  
  lynx --dump --nolist "https://www.ncbi.nlm.nih.gov/pubmed/?term=$word+AND+$((year1+i))[pdat]&dispmax=$papers&report=abstract"> "output$i.txt"
  if [ $related != $none ]
  then
     lynx -dump "https://www.ncbi.nlm.nih.gov/pubmed/?term=$word+AND+$((year1+i))[pdat]&dispmax=$papers&report=abstract" | awk '/http/{print $2}' > "links$i$user_id"
     sed -i '/linkname=pubmed_pubmed&from_uid/!d' "links$i.txt"
     mapfile -t arr < "links$i$user_id.txt"
     len=${#arr[@]}
     rm "links$i$user_id"
     for j in ${arr[*]}
     do 
       k=$((k+1))
       lynx --dump --nolist "$j&dispmax=$related&report=abstract" > "related$k$user_id.txt"
     done
  fi
done

cat *txt > testfile 

for ((i=0;i<=$numyears;i++))
do
   rm "output$i$user_id.txt"
done


if [ $related != $none ]
then
  for ((i=0;i<=$k;i++))
  do
   rm "related$i$user_id.txt"
  done
fi


sed -i 's/[ \t]*//' testfile
sed -i '/^[[:space:]]*$/d' testfile
awk 'length($0)>50' testfile > out
rm testfile 
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
