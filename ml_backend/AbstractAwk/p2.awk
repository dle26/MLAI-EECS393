BEGIN {
      ORS=" "
      n = make_array("stop",stopwords)
      n = make_array("spanishwords",spanish)
      n = make_array("searchwords",searchwords)
      normalize = 0
      skipword = 1
      found_keyword = 0
      split(topic,topic_arr,"+") 
      for (i in topic_arr)
        topic_words[topic_arr[i]] = topic_arr[i]
      }
      
{
for (i=1; i <= NF;i++)
{
### eliminate stopwords 
if ($i in stopwords || $i in spanish ||$i in topic_arr || length($i) < 4 || i==NF)
   continue
if ($(i+1) in stopwords || $(i+1) in spanish || $(i+1) in topic_arr || length($(i+1)) < 4)
   stopword = 0

if ($i in searchwords)
{
   found_keyword = 1
   keywords[$i] = 1
}

bigram = $i" "$(i+1)
if ($i in allwords)
{ 
  allwords[$i] = allwords[$i] + 1
}
else
{
allwords[$i] = 1
}

if (!($i in seenwords))
  {
   seenwords[$i] = $i
   }
 }
 
if (bigram in allbigrams && stopword == 1)
{ 
 allbigrams[bigram] = allbigrams[bigram]+1
 }
 
if (!(bigram in allbigrams) && stopword == 1)
{ 
 allbigrams[bigram] = 1
} 

 if (!(bigram in seenbigrams))
  {
    seenbigrams[bigram] = bigram
  }
}
if (NR%20==0)
   {
     if (found_keyword == 1)
     {
     for (j in seenwords)
     {
       for (x in keywords)
       {
         if (!(j == x))
         {
          if (x"-"j in wordcounts)
             wordcounts[x"+"j] += 1
          else
            wordcounts[x"+"j] = 1   
         }
        }
     }

     for (k in seenbigrams)
     {
       for (x in keywords)
         {
            if (x"-"k in bigramcounts)
             bigramcounts[x"+"k] += 1
          else
            bigramcounts[x"+"k] = 1   
         }
     }
     
      found_word = 0
     }
     
     delete seenwords
     delete seenbigrams
     delete keywords
     normalize = normalize + 1
    }
    
stopword = 1
   }
}


END {
    j=0
    for (i  in wordcounts)
       {
        numwordcounts[j] = wordcounts[i]
        words[j] = i
        j+=1
       }
    n =  dual_insertion_sort(numwordcounts,words) 
    for (i=int(length(wordcounts)); i >= int(length(wordcounts)*0.5);i--)
        {
           print numallwords[i]":"(numwordcounts[i]/normalize)
           print "\n"
        }

    j=0
    for (i  in bigramcounts)
       {
        numbigramcounts[j] = bigramcounts[i]
        bigrams[j] = i
        j+=1
       }
       
    n =  dual_insertion_sort(numbigramcounts,bigrams)
    for (i=int(length(bigramcounts)); i >= int(length(bigramcounts)*0.5);i--)
        {
           print numallbigrams[i]";"(numbigramcounts[i]/normalize)
           print "\n"
        }
     
    j=0
    for (i  in allwords)
       {
        numallwords[j] = allwords[i]
        total_words[j] = i
        j+=1
       }
     
     n =  dual_insertion_sort(numbigramcounts,bigrams)
    for (i=int(length(allwords)); i >= int(length(allwords)*0.5);i--)
        {
           print numallwords[i]"#"(total_words[i]/normalize)
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
