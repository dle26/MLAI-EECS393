BEGIN {
      ORS=" "
      n = make_array("stop",stopwords)
      n = make_array("spanishwords",spanish)
      normalize = 0
      split(topic,topic_arr,"+") 
      for (i in topic_arr)
        topic_words[topic_arr[i]] = topic_arr[i]
      }
{
for (i=1; i <= NF;i++)
{
### eliminate stopwords 
if ($i in stopwords || $i in spanish ||$i in topic_arr || $i in seenwords || length($i) < 4)
   continue 

seenwords[$i] = $i
if ($i in allwords)
{ 
   wordcounts[$i] = wordcounts[$i] + 1
}
else
{
   wordcounts[$i] = 1
   allwords[$i] = $i
}
if (NR%50==0)
   {
     delete seenwords
     normalize = normalize + 1
    }
   }
}


END {
    j=0
    for (i  in wordcounts)
       {
        numwordcounts[j] = wordcounts[i]
        numallwords[j] = allwords[i]
        j+=1
       }
    n =  dual_insertion_sort(numwordcounts,numallwords) 
    for (i=int(length(wordcounts)*0.95); i >= int(length(wordcounts)*0.9);i--)
        {
           print numallwords[i]": "(numwordcounts[i]/normalize)*100
           print "\n"
        }
}


function make_array(file, array)
  {
   status = 1;

   while (status > 0) {
      status = getline record < file
      array[record] = record;
   }
   close(file);
   return tracker
}


function dual_insertion_sort(arr1,arr2)
{
 for(i=0; i < length(arr1); i++)
 {
    value = arr1[i]
    value2 = arr2[i]
    j = i - 1
    while( ( j > 0) && (arr1[j] > value)) {
      arr1[j+1] = arr1[j]
      arr2[j+1] = arr2[j]
      j--
    }
    arr1[j+1] = value
    arr2[j+1] = value2
  }
  return 0
  }


