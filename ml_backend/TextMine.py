#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:19:49 2020

@author: anibaljt
"""

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
import json
import nltk
import itertools
import requests
import numpy as np
from nltk.corpus import stopwords
import string
from nltk.corpus import wordnet as wn
import pickle
import os
nltk.download('wordnet')
import datetime




class TEXTMINE:
    
    
    TECHNICAL_KEYWORDS = ["machine learning","deep learning","clustering",
                          "supervised learning","computer vision"]
    
    def __init__(self,user_keywords,technical_keywords):
        
        self.user_keywords = user_keywords
        self.technical_keywords = technical_keywords
        self.run_id = run_id
    
    def from_database(self):
        
        con_file = open("config.json")
        config = json.load(con_file)
        con_file.close()
        client = ElsClient(config['apikey'])
        header = {'X-ELS-APIKey': config['apikey'],
          'Accept':'text/plain'}
        
        now = datetime.datetime.now()
        
        years = list(range(now.year-1,now.year+1))
        
        bigrams = []
        bigram_scores = []
        
        for year in years:
          for combo in self.generate_combinations(self.user_keywords,TEXTMINE.TECHNICAL_KEYWORDS):
              
             file = open("TextMineResults" + str(self.run_id) + ".txt","w")
            
             string = combo[0] + " " + combo[1]
             doc_srch = ElsSearch(string + ' ' + str(year),'sciencedirect')
             doc_srch.execute_modified(doc_srch.uri,client,get_all=True,set_limit=75,get_all = True)

             for num,res in enumerate(doc_srch.results):
                 
                 DOI = res['prism:doi']
                 URL = 'https://api.elsevier.com/content/article/DOI/' + str(DOI) + '?view=FULL"
                 r = requests.get(url = URL,headers=header)
                 
                 if 'INVALID_INPUT' not in str(r.content):
                     file.write(str(r.content))
                     
             file.close()
             subprocess.check_call(["abstractawk.sh",str(file),str(self.user_id)])
        
             with open("results" + str(self.user_id)) as f:
                lines = f.readlines()
                for ln in lines:
                    bigrams.append(ln[0:ln.index(":")])
                    bigram_scores.append(float(ln[ln.index(":")+1:len(ln)]))
                    shutil.rmtree("results" + str(self.user_id))
        
        return self.two_list_sort(bigrams,bigram_scores)
        
        
    def generate_combinations(self,l1,l2):
        
        combinations = []
        permutations = itertools.permutations(l1, 2)
        for perm in permutations:
            zipped = zip(perm, l2)
            combinations.append(list(zipped))
        return combinations
    
    
    ### TODO: CITE ELSAPY - I MODIFIED THE SRC FOR MLAI 
    def execute_modified(uri,els_client = None, get_all = False,set_limit=25):

        api_response = els_client.exec_request(uri
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
    
     
    def format_keywords(self):
       pass
