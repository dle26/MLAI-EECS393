#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt

"""

import string
import numpy as np

class TEXTPROCESS: 
    
    def findkeywords(file,searchwords,user_input):
        
         tracker = 0
         allresults = {}
         num_matches = 0
         allwords = []
         punctuation = list(string.punctuation)
         punctuation.remove('-')
         
         user_words =""
         user_bigrams = ""
         
         for tup in user_input:
             if user_words.find(tup[0]) == -1:
                 user_words += (tup[0] + " ")
                 if len(tup[0].split()) > 1:
                     if user_bigrams.find(tup[0]) == -1:
                        if tup[0].split()[0] != "":
                            user_bigrams += (tup[0].split()[0] + " " + tup[0].split()[1] + "+")
                                
             if len(tup[1]) > 1:
                if user_words.find(tup[1]) == -1:
                    user_words += (tup[1] + " ")
                if len(tup[1].split()) > 1:
                    if user_bigrams.find(tup[1]) == -1:
                        if tup[1].split()[1] != "":
                            user_bigrams += (tup[1].split()[0] + " " + tup[1].split()[1] + "+")

         user_bigrams = user_bigrams[0:-1]
        
         with open(file,'r') as f:
             
            lines = f.readlines()
            for n,l in enumerate(lines):

              seenwords = []
              results = {}
              num_matches = 0
              l = str(l)
              
              if len(l) > 500:

                 tracker += 1
                 
                 l.translate(punctuation)
                 split_l = l.split()
                 split_l = [ln.lower() for ln in split_l]
                 allwords.extend(split_l)
                 
                 for key in searchwords:
                     for word in searchwords[key]:
                        if l.lower().find(word) > -1 and word not in seenwords:
                            results[word] = 1
                            seenwords.append(word)
                            
                            if word not in split_l:     
                                allwords.append(word)
                                
                 if user_bigrams != "":
                   for bigram in user_bigrams.split('+'):
                      if l.find(bigram) > -1 and len(results)>0:
                          if bigram.split()[0] not in seenwords and bigram.split()[1] not in seenwords:
                               num_matches+=1 
                          seenwords.extend([bigram.split()[0],bigram.split()[1]])
                 
                           
                 for word in user_words.split():
                     if l.find(word) > -1 and len(results)>0:
                       if word not in seenwords:
                           num_matches += 1
                       seenwords.append(word)

                 #### adjust based on num of matches per word in  that section (robustness of match)
                 for word in results:
                   if num_matches > 0:
                     if word in allresults:
                         allresults[word] += results[word] *(num_matches/len(user_input))
                     else:
                         allresults[word] = results[word] *(num_matches/len(user_input))
                 
         f.close()

         if len(allresults) == 0:
             return {},{}
         
         for word in allresults:
             if word in searchwords['specific'] and word not in searchwords['category']:
                allresults[word] = (allresults[word]/tracker) #+ ((allresults[word]/tracker)*0.1))
             else:
                 allresults[word] = (allresults[word]/tracker)
                 

         return allresults,allwords
     
    
    ###TODO: pattern matching by percentage??
    def string_match():
        pass
