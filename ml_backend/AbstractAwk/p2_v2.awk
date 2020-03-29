BEGIN {
      ORS=" "
      n = make_array("stop",stopwords)
      n = make_array("spanishwords",spanish)
      normalize = 0
      skipword = 1
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
 
bigram = $i" "$(i+1)
if ($i in allwords)
{ 
  if (!($i in seenwords))
  {
   wordcounts[$i] = wordcounts[$i] + 1
   }
}
else
{
 if (!($i in seenwords))
  {
   allwords[$i] = $i
   wordcounts[$i] = 1
   }
 }

if (bigram in allbigrams && stopword == 1)
{ 
 if (!(bigram in seenbigrams))
  {
   bigramcounts[bigram] = bigramcounts[bigram] + 1
   }
}
else
{
 if (stopword == 1)
  {
    if (!(bigram in seenbigrams))
    {
   bigramcounts[bigram] =  1
   allbigrams[bigram] = bigram
   }
   }
}
if (NR%50==0)
   {
     delete seenwords
     delete seenbigrams
     normalize = normalize + 1
    }
seenbigrams[bigram] = bigram
seenwords[$i] = $istopword = 1
stopword = 1
   }
}


END {
    print "<pre>"
    print "<h1> --- Your Topic --- </h1>"
    print "\n"
    print topic
    print "\n"
    print "\n"
    print "<h1> ---- Keywords (Scores typically between 0.5-5, higher score = hotter topic!) ---- </h1>"
    print "\n" 
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

    print "\n"
    print "\n"
    print "<h1> ---- Key Bigrams (Scores typically between 0.5-5, higher score = hotter topic!) ---- </h1>"
    j=0
    for (i  in bigramcounts)
       {
        numbigramcounts[j] = bigramcounts[i]
        numallbigrams[j] = allbigrams[i]
        j+=1
       }
    n =  dual_insertion_sort(numbigramcounts,numallbigrams)
    for (i=int(length(bigramcounts)*0.95); i >= int(length(bigramcounts)*0.9);i--)
        {
           print numallbigrams[i]": "(numbigramcounts[i]/normalize)*100
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


