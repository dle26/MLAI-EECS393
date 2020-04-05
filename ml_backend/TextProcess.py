#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 00:06:16 2020

@author: anibaljt
"""

import string

class TEXTPROCESS: 
    
    
    def findkeywords(file,searchwords,user_input):
        
         ### TODO: SYNONYMS
         tracker = 0
         results = {}
         user_matches = 0
         allwords = []
         
         with open(file,'r') as f:
            lines = f.readlines()
            for n,l in enumerate(lines):
              seenwords = []
              if len(l) > 500:
                 tracker += 1
                 l.translate(string.punctuation)
                 l = l.split()
                 l = [ln.lower() for ln in l]
                 allwords.extend(l)
                 for key in searchwords:
                     for word in searchwords[key]:
                        if str(l) .find(word) > -1 and word not in seenwords:
                            if word in results:
                                results[word] += 1
                            else:
                                results[word] = 1
                            seenwords.append(word)
                            
                 for word in l:
                     if user_input.find(word) > -1 and word not in seenwords:
                         user_matches += 1
                         seenwords.append(word)
                            
         f.close()
         
         for word in results:
             results[word] = results[word]*(user_matches/tracker*len(user_input))
             
         return results,allwords,tracker
     
        
    def string_match():
        pass