#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:19:49 2020

@author: anibaljt
"""

import elsapy
from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
import json
import itertools
import inspect
import requests
import numpy as np
import pickle
import os
import datetime
from sklearn.preprocessing import MinMaxScaler
import MLTechniques
import subprocess


class TEXTMINE:
    
    
    SUP_TECHNICAL_KEYWORDS = ["machine learning","deep learning",
                          "supervised learning","classification","preprocessing","scaling"]
    
    UNS_TECHNICAL_KEYWORDS = ["machine learning","deep learning",
                          "unsupervised learning","clustering","preprocessing","scaling"]
    
    
    def __init__(self,user_keywords,user_id,analysis_type='supervised'):
        
        self.user_keywords = user_keywords
        self.user_id = user_id
        self.analysis_type = analysis_type

        
    def from_database(self):
        
        if self.analysis_type == 'supervised':
            tech_words = TEXTMINE.SUP_TECHNICAL_KEYWORDS
            
        elif self.analysis_type == 'unsupervised': 
             tech_words = TEXTMINE.UNS_TECHNICAL_KEYWORDS


        con_file = open("config.json")
        config = json.load(con_file)
        con_file.close()
        client = ElsClient(config['apikey'])
        header = {'X-ELS-APIKey': config['apikey'],
          'Accept':'text/plain'}

        ###TODO: add year back in??
        
        search_words = open("searchwords","w")
        techniques = []
        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
                if obj.TECHNIQUE_TYPE == self.analysis_type or obj.TECHNIQUE_TYPE == 'preprocessing':
                    if obj.get_category_name() not in techniques:
                        search_words.write(obj.get_category_name() + '\n')
                        techniques.append(obj.get_category_name())
   
        
        search_words.close()
        
        for combo in self.generate_combinations(self.user_keywords,tech_words):
              
             file = open("TextMineResults" + str(self.user_id) + ".txt","w")
             

             if len(combo[0][0]) == 2:

                 string = combo[0][0][0] + " " + combo[0][0][1] + " " + combo[0][1]
             else:
                 string = combo[0][0][0] + " " + combo[0][1]
                 
             doc_srch = ElsSearch(string,'sciencedirect')
             results = TEXTMINE.execute_modified(doc_srch.uri,client,get_all=True,set_limit=25)

             for num,res in enumerate(results):
                 
                 DOI = res['prism:doi']
                 URL = 'https://api.elsevier.com/content/article/DOI/' + str(DOI) + "?view=FULL"
                 r = requests.get(url = URL,headers=header)
                 
                 if 'INVALID_INPUT' not in str(r.content):
                     file.write(str(r.content))
                     
             file.close()
             subprocess.check_call(["AbstractAwk/abstractawk.sh",str(file),str(search_words),str(self.user_id)])
             os.remove(file)
             filename = "results" + self.user_id
             keywords,keyword_scores = self.adjust_awk_output(filename)
        
        os.remove(search_words)
        
        return self.two_list_sort(keywords,keyword_scores)
        
        
    
    def generate_combinations(self,l1,l2):
        
        combinations = []
        permutations = itertools.permutations(l1, 2)
        for perm in permutations:
            zipped = zip(perm, l2)
            combinations.append(list(zipped))
        return combinations
    
    
    
    ### TODO: CITE ELSAPY - I MODIFIED THE SRC FOR MLAI 
    def execute_modified(uri,els_client = None, get_all = False,set_limit=25):

        api_response = els_client.exec_request(uri)
        results = api_response['search-results']['entry']
        
        if get_all is True:
           i = 0
           while i<(int(set_limit/25)-1):
            for e in api_response['search-results']['link']:
                    if e['@ref'] == 'next':
                        next_url = e['@href']
            api_response = els_client.exec_request(next_url)
            results += api_response['search-results']['entry']
            i += 1
    
        return results
    
               
                                
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
    
    
     
    def adjust_awk_output(self,file):

      keywords = []
      keyword_scores = []
      
      #### SKIPGRAM HERE -- generate synonyms/related words
      
      with file as f:
         tracker = 0
         lines = f.readlines()
         for ln in lines:
             if ln.find(':') > -1:
                 keywords.append(ln[0:ln.index(":")])
                 keyword_scores.append(float(ln[ln.index(":")+1:len(ln)]))
             if ln.find(';') > -1:
                 keywords.append(ln[0:ln.index(";")])
                 keyword_scores.append(max(1,float(ln[ln.index(";")+1:len(ln)])+(0.1*float(ln[ln.index(";")+1:len(ln)]))))
             if ln.find("#") == -1:
                tracker += 1
             else:
                 keyword_scores[keywords.index(ln[0:ln.index("#")])] = (keyword_scores[keywords.index(ln[0:ln.index("#")])]/float(ln[ln.index("#")+1:len(ln)]))
                                                             
      os.remove(file)
      
      return list(MinMaxScaler().fit_transform(keywords)),keyword_scores