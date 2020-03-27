#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 00:42:59 2020

@author: anibaljt
"""


import subprocess
import shutil
import itertools




class AbstractAwk:
    
    
    def __init__(self,user_keywords,technical_keywords,run_id):
        
        self.user_keywords = user_keywords
        self.technical_keywords = technical_keywords
        self.run_id = run_id
    
    
    def run_AA(self):

        keywords = self.generate_combinations(self.user_keywords,self.technical_keywords)
        keywords = self.format_keywords(keywords)
        bigram_scores = []
        bigrams = []
        

        for keyword in keywords:
            
            ### TODO: remove html outputs and format results file, add the additional parameters

            subprocess.check_call(["abstractawk.sh",keyword,"2018","2020","200","50",str(self.user_id)])
            with open("results" + str(self.user_id) + ".txt") as f:
                lines = f.readlines()
                for ln in lines:
                    bigrams.append(ln[0:ln.index(":")])
                    bigram_scores.append(float(ln[ln.index(":")+1:len(ln)]))
            shutil.rmtree("results" + str(self.user_id))
        
        return self.two_list_sort(bigrams,bigram_scores)[int(len(bigrams)*0.9):len(bigrams)]
            
        
    def generate_combinations(self,l1,l2):
        
        combinations = []
        permutations = itertools.permutations(l1, 2)
        for perm in permutations:
            zipped = zip(perm, l2)
            combinations.append(list(zipped))
        return combinations
        
    
    def format_keywords():
        
        keywords = []
        for tup in keywords:
            keywords.append(str(tup[0])+"+"+str(tup[1]))
        return keywords

       
    
    def two_list_sort(self,tosort,basis):
        
      for i in range(1, len(basis)):
        key = basis[i]
        key2 = tosort[i]
        j = i-1
        while j >=0 and key <basis[j] : 
                basis[j+1] = basis[j] 
                tosort[j+1] = tosort[j]
                j -= 1
                
        basis[j+1] = key 
        tosort[j+1] = key2
        
      return tosort
