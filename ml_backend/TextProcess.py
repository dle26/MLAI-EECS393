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
         user_matches = {}
         num_matches = 0
         allwords = []
         all_matches = {}

         with open(file,'r') as f:
             
            lines = f.readlines()
            for n,l in enumerate(lines):

              seenwords = []
              results = {}
              num_matches = 0
              l = str(l)
              
              if len(l) > 500:

                 tracker += 1
                 l.translate(string.punctuation)
                 split_l = l.split()
                 split_l = [ln.lower() for ln in split_l]
                 allwords.extend(split_l)
                 for key in searchwords:
                     for word in searchwords[key]:
                         
                        if l.lower().find(word) > -1 and word not in seenwords:
 
                            if word in results:
                                results[word] += 1
                            else:
                                results[word] = 1
                            seenwords.append(word)
                            
                            if word not in split_l:     
                                allwords.append(word)
                            
                 for word in split_l:
                     if user_input.find(word) > -1:
                       if word not in seenwords:
                           
                           if word in user_matches:
                               user_matches[word] += 1
                           else:
                               user_matches[word] = 1
                        
                           seenwords.append(word)
                           num_matches += 1
     
                       if word in all_matches:
                          all_matches[word] += 1
                       else:
                          all_matches[word] = 1
                    
                    
                         
                 #### adjust based on num of matches per word in that section
                 for word in results:
                     if word in allresults:
                         allresults[word] += results[word]*(num_matches/len(user_input))
                     else:
                         allresults[word] = results[word]*(num_matches/len(user_input))
                            
         f.close()
         
         #### adjust based on number of lines containing any match
         for word in user_matches:
             user_matches[word] /= all_matches[word]
            
         
         ### Adjust based on estimated use frequency of user input words
         #### TODO: adjust??
         
         for word in allresults:
             allresults[word] = (allresults[word]/tracker)*np.median(list(user_matches.values()))
             
         return allresults,allwords,tracker
     
        
    def string_match():
        pass