BEGIN {
      ORS=" "
      n = make_array("stop",stopwords)yx
      n = make_array("foundwords",searchwords)
      normalize = 0
      total_words = 0
      total_bigrams = 0
      stopword = 1
      validword = 1
      found_word = 0
      total_keywords
     
      }
      
{
for (i=1; i <= NF;i++)
{

### eliminate stopwords 
if (i==1 || i==NF || $i in stopwords || length($i) < 3 || length($i) > 50)
   validword = 0
   
if ($(i+1) in stopwords || length($(i+1)) < 3 || length($(i+1)) > 50)
   stopword = 0
   
if (validword == 1)
{
total_words += 1

if ($i in searchwords)
{  
   if ($i in keyword_counts)
      keyword_counts[$i] += 1
   else
      keyword_counts[$i] = 1
   total_keywords += 1
}

if (stopword == 1)
    { 
     bigram = $i" "$(i+1)
     total_bigrams += 1
    }
    
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

if (NR%50==0 && i==NF-1)
   { 
    for (x in searchwords)
     {
     for (j in seenwords)
     { 
        if (x in seenwords && !(x==j))
        {
          if (x"-"j in wordcounts)
             wordcounts[x"-"j] += 1.1
          else
            wordcounts[x"-"j] = 1.1
         }
         else
         { 
           if (x"-"j in wordcounts)
             wordcounts[x"-"j] += 1
          else
            wordcounts[x"-"j] = 1
         }
     }}
     for (k in seenbigrams)
     {
        for (x in searchwords)
         {
           if (index(k,x) > 0) 
           {
           if (x"-"k in bigramcounts)
               bigramcounts[x"-"k] += 1.1
          else
            bigramcounts[x"-"k] = 1.1   
           }
           else
           {
          if (x"-"k in bigramcounts)
               bigramcounts[x"-"k] += 1
          else
            bigramcounts[x"-"k] = 1 
           }
     }
     }
     
     delete seenwords
     delete seenbigrams
     normalize = normalize + 1
   }
  stopword = 1
  validword = 1
   }
}

END {
    j=0
    for (i in wordcounts)
       {
        numwordcounts[j] = wordcounts[i]
        words[j] = i
        j+=1
       }
       
    n = dual_insertion_sort(numwordcounts,words) 
    for (i=int(length(wordcounts))-1; i >= int(length(wordcounts)*0.5);i--)
        {
           n = split(words[i], arr, "-")
           print words[i]":"(numwordcounts[i]/normalize)*(allwords[arr[2]]/total_words)*(keyword_counts[arr[1]]/total_keywords)
           print "\n"
        }

    j=0
    for (i in bigramcounts)
       {
        numbigramcounts[j] = bigramcounts[i]
        bigrams[j] = i
        j+=1
       }
       
    n =  dual_insertion_sort(numbigramcounts,bigrams)
    
    for (i=int(length(bigramcounts))-1; i >= int(length(bigramcounts)*0.5);i--)
        {
           n = split(bigrams[i], arr, "-")
           print bigrams[i]";"(numbigramcounts[i]/normalize)*(allbigrams[arr[2]]/total_bigrams)*(keyword_counts[arr[1]]/total_keywords)
           print "\n"
        }
     
    j=0
    for (i in allwords)
       {
        numallwords[j] = allwords[i]
        total_words2[j] = i
        j+=1
       }
     
    n =  dual_insertion_sort(numallwords,total_words2)
    for (i=int(length(allwords))-1; i >= int(length(allwords)*0.5);i--)
        {
           print total_words2[i]"#"(numallwords[i]/total_words)
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
