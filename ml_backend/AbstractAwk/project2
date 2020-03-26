#!/bin/bash

read -p "Enter your topic here (i.e. virus, hay+fever): " word
read -p "Search papers published in or after (i.e. 2016): " year1
read -p "Search papers published in or before (i.e. 2020): " year2
read -p "How many papers per search year (5,10,20,50,100,200): " paper
read -p "How many related papers in search (None,5,10,20,50,100,200): " related

none="None"
numyears=$((year2-year1))
k=0

for ((i=0; i<=$numyears;i++))
do  
  lynx --dump --nolist "https://www.ncbi.nlm.nih.gov/pubmed/?term=$word+AND+$((year1+i))[pdat]&dispmax=$papers&report=abstract"> "output$i.txt"
  if [ $related != $none ]
  then
     lynx -dump "https://www.ncbi.nlm.nih.gov/pubmed/?term=$word+AND+$((year1+i))[pdat]&dispmax=$papers&report=abstract" | awk '/http/{print $2}' > "links$i"
     sed -i '/linkname=pubmed_pubmed&from_uid/!d' "links$i.txt"
     mapfile -t arr < "links$i.txt"
     len=${#arr[@]}
     rm "links$i"
     for j in ${arr[*]}
     do 
       k=$((k+1))
       lynx --dump --nolist "$j&dispmax=$related&report=abstract" > "related$k.txt"
     done
  fi
done

cat *txt > testfile 

for ((i=0;i<=$numyears;i++))
do
   rm "output$i.txt"
done


if [ $related != $none ]
then
  for ((i=0;i<=$k;i++))
  do
   rm "related$i.txt"
  done
fi


sed -i 's/[ \t]*//' testfile
sed -i '/^[[:space:]]*$/d' testfile
awk 'length($0)>50' testfile > out
sed -i 's/[0-9]\w\+//g' out
sed -i 's/[]/.:;<>!=+?,"&@%()[^*]//g' out
sed -i 's/\\//g' out
sed -i 's/[A-Z]/\L&/g' out
sed -i '/^$/d' stop
sed -i 's/[[:space:]]*$//' stop
sed -i '/^$/d' spanishwords
sed -i 's/[[:space:]]*$//' spanishwords
awk -v topic=$word -f p2.awk out > results.html
rm testfile
rm out

