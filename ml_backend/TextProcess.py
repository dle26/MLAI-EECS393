#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 00:06:16 2020

@author: anibaljt
"""

import string
import nltk

class TEXTPROCESS: 
    
    
    def findkeywords(file,searchwords):
        
         results = []
        
         with open(file,'rb') as f:
            lines = f.readlines()
            for l in lines[100:len(lines)]:
                for word in searchwords:
                    if str(l).find(word) > -1:
                        results.append(word)
                        searchwords.remove(word)
                    if len(searchwords) == 0:
                        return results
         f.close()
         return results
        
                        
                        
                        
        
    def process_score(file,foundwords):
        
        normalize = 0
        total_words = 0
        total_bigrams = 0
        stopword = False
        validword = False
        found_word = False
        total_keywords = 0
        keyword_counts = {}
        seenwords = []
        seenbigrams = []
        allwords = {}
        allbigrams = {}
        wordcounts = {}
        bigramcounts = {}
        
        with open(file,'rb') as f:
            
            lines = f.readlines()
            for n,line in enumerate(lines[100:len(lines)]):
                line = str(line)
                line.translate(string.punctuation)
                words = line.split()
                words = nltk.pos_tag([x.lower() for x in words])
                
                for k,tup in enumerate(words):
                    
                   if checkword(tup):
                       validword = True
                   if k < len(words)-1:
                       if checkbigram(words,k):
                           stopword = True
                       
                   if validword:
                       total_words += 1
                       i = tup[0]
                       if i in foundwords:
                           found_word = True
                           if i in keyword_counts:
                               keyword_counts[i] += 1
                       else:
                            keyword_counts[i] = 1
                       total_keywords += 1

                       if i in allwords:
                           allwords[i] = allwords[i] + 1
                       else:
                           allwords[i] = 1

                       if i in seenwords:
                           seenwords.append(i)
                       
                   if stopword:
                       bigram = i + " " + words[k+1][0]
                       total_bigrams += 1

                       if bigram in allbigrams and stopword:
                           allbigrams[bigram] = allbigrams[bigram]+1
 
                       if (bigram not in allbigrams) and stopword: 
                            allbigrams[bigram] = 1

                       if bigram not in seenbigrams:
                           seenbigrams[bigram] = bigram

                if (n==50):
                    for x in foundwords:
                        for j in seenwords:
                            if x in seenwords and x !=j:
                                if (x + "-" + j in wordcounts):
                                    wordcounts[x + "-" + j] += 1.1
                                else:
                                    wordcounts[x + "-" + j] = 1.1

                            else:
                                if (x + "-" + j in wordcounts):
                                    wordcounts[x + "-" + j] += 1
                                else:
                                    wordcounts[x + "-" + j] = 1
     
                        for k in seenbigrams:
                            for x in foundwords:
                                if (k.find(x) > -1): 
                                    if (x + "-" +k in bigramcounts):
                                        bigramcounts[x + "-" + k] += 1.1
                                    else:
                                        bigramcounts[x + "-" + k] = 1.1   
                                else:
                                    if (x + "-" + k in bigramcounts):
                                        bigramcounts[x + "-" + k] += 1
                                    else:
                                        bigramcounts[x + "-" + k] = 1 

                        seenwords = []
                        seenbigrams = []
                        normalize += 1

                    stopword = False
                    validword = False
        f.close()
          
        if found_word:
            for word in wordcounts:
                word_sp = word.split("-")
                wordcounts[word] = (wordcounts[word]/normalize)*(allwords[word_sp[1]]/total_words)*(keyword_counts[word_sp[0]]/total_keywords)

            wordcounts = key_sort(wordcounts) 
        
            for bg in bigramcounts:
                bg_sp = bg.split("-")
                bigramcounts[word] = (bigramcounts[bg]/normalize)*(allbigrams[bg_sp[0]]/total_bigrams)*(keyword_counts[bg_sp[0]]/total_keywords)

            bigramcounts = key_sort(bigramcounts)

            for word in allwords:
                allwords[word] = allwords[word]/total_words

        return list(wordcounts.keys()),list(wordcounts.values()),list(bigramcounts.keys()),list(bigramcounts.values()),list(allwords.keys()),list(allwords.values())





def key_sort(keys,values): 
  
   for i in range(1, len(values)): 
            
      key = values[i] 
      key2 = keys[i]
            
      j = i-1
      while j >=0 and key < values[j] : 
          values[j+1] = values[j] 
          keys[j+1] = values[j]
          j -= 1
      values[j+1] = key 
      keys[j+1] = key2
            
      return keys,values



def checkword(tup):
    
    if tup[1][0] == 'N':
        return True
    return False

def checkbigram(words,k):
    
    if (words[k][1][0] == 'N' and words[k+1][1][0] == 'J') or (words[k][1][0] == 'J' and words[k+1][1][0] == 'N'):
        return True
    return False

    
        