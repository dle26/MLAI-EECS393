BEGIN {
      ORS=" "
      n = make_array("stop",stopwords)
      n = make_array("spanishwords",spanish)
      n = make_array("searchwords",searchwords)
      normalize = 0
      total_words = 0
      total_bigrams = 0
      stopword = 1
      validword = 1
      found_keyword = 0
      total_keywords
      }
      
{
for (i=1; i <= NF;i++)
{

### eliminate stopwords 
if ($i in stopwords || $i in spanish || length($i) < 3 || length($i) > 50)
   validword = 0
   
if ($(i+1) > NF || $(i+1) in stopwords || $(i+1) in spanish || length($(i+1)) < 3 || length($(i+1)) > 50)
   stopword = 0
   
if (validword == 1)
{
total_words += 1

if ($i in searchwords)
{
   if ($i in keyword_count)
      keyword_count[$i] += 1
   else
      keyword_count[$i] = 1
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

if (NR%50==0 && i==NF)
   { 
    for (x in searchwords)
     {
     for (j in seenwords)
     { 
        if (x in seenwords && x==j)
        {
          if (j in wordcounts)
             wordcounts[x" "j] += 1.1
          else
            wordcounts[x" "j] = 1.1
         }
         else
         { 
           if (j in wordcounts)
             wordcounts[x" "j] += 1
          else
            wordcounts[x" "j] = 1
         }
     }
     for (k in seenbigrams)
     {
        for (x in searchwords)
         {
           if (k ~ x)
           {
           if (x"-"k in bigramcounts)
               bigramcounts[x"+"k] += 1.1
          else
            bigramcounts[x"+"k] = 1.1   
           }
           else
           {
          if (x"-"k in bigramcounts)
               bigramcounts[x"+"k] += 1
          else
            bigramcounts[x"+"k] = 1 
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
    if (found_word == 1)
    {
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
           n = split(words[i], arr, " ")
           print words[i]":"(numwordcounts[i]/normalize)*(allwords[words[i]]/total_words)*(keyword_counts[arr[0]]/total_keywords)
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
           n = split(bigrams[i], arr, " ")
           print bigrams[i]";"(numbigramcounts[i]/normalize)*(allbigrams[bigrams[i]]/total_bigrams)*(keyword_counts[arr[0]]/total_keywords)
           print "\n"
        }
     
    j=0
    for (i  in allwords)
       {
        numallwords[j] = allwords[i]
        total_words2[j] = i
        j+=1
       }
     
    n =  dual_insertion_sort(numallwords,total_words2)
    for (i=int(length(allwords)); i >= int(length(allwords)*0.5);i--)
        {
           print total_words2[i]"#"(numallwords[i]/normalize)
           print "\n"
        }
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
