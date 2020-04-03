#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:19:49 2020

@author: anibaljt
"""

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
import json
import itertools
import inspect
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
import MLTechniques
import subprocess
import time
from TextProcess import TEXTPROCESS


class TEXTMINE:
    
    
    SUP_TECHNICAL_KEYWORDS = ["machine learning","deep learning",
                          "supervised learning","classification","preprocessing"]
    
    UNS_TECHNICAL_KEYWORDS = ["machine learning","deep learning",
                          "unsupervised learning","clustering"]
    
    
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
        ###TODO: add year back in??
        searchwords = []

        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
                if obj.TECHNIQUE_TYPE == self.analysis_type:
                    if obj.get_category_name():
                        searchwords.append(obj.get_category_name())


        textmine_results_words = {'words':[],'scores':[]}
        textmine_results_bg = {'bigrams':[],'scores':[]}
        textmine_results_allwords = {'words':[],'scores':[]}
        
        for n,combo in enumerate(self.generate_combinations(self.user_keywords,tech_words)):
              
             if len(combo[0][0]) == 2:

                 string = combo[0][0][0] + " " + combo[0][0][1] + " " + combo[0][1]
             else:
                 string = combo[0][0][0] + " " + combo[0][1]
                 
             doc_srch = ElsSearch(string, 'sciencedirect')
             results = TEXTMINE.execute_modified(doc_srch.uri,client,get_all=True,set_limit=25)

             for num,res in enumerate(results):
                 print("STARTING NEW ONE")
                 DOI = res['prism:doi']
                 URL = 'https://api.elsevier.com/content/article/DOI/' + str(DOI) + "?APIKey=" + str(config['apikey'])
                 
                 subprocess.Popen(["bash",str(os.getcwd()) + "/collect.sh",str(URL), str(self.user_id)])
                 time.sleep(1)

                 
                 foundwords = TEXTPROCESS.findkeywords(str(self.user_id),searchwords)
                 results = TEXTPROCESS.process_score(str(self.user_id),foundwords)
                 os.remove(str(self.user_id))
                 textmine_results_words['words'].extend(results[0])
                 textmine_results_words['scores'].extend(results[1])
                 textmine_results_bg['bigrams'].extend(results[2])
                 textmine_results_bg['scores'].extend(results[3])
                 textmine_results_allwords['words'].extend(results[4])
                 textmine_results_allwords['scores'].extend(results[5])
                
        keywords,keyword_scores = self.adjust_output(textmine_results_words,textmine_results_bg,textmine_results_allwords)

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
    
    
     
    def adjust_output(self,words,bigrams,allwords):

      scores = []
      wscores = []
            
      allwordkeys = np.asarray(list(set(list(allwords.keys()))))
      for word in allwordkeys:
          wscores.append(np.median(np.asarray(list(allwords.values()))[np.where(np.asarray(list(allwords.keys())) == word)]))
          
      wordkeys = np.asarray(list(set(list(words.keys()))))
      for word in wordkeys:
          scores.append(np.median(np.asarray(list(words.values()))[np.where(np.asarray(np.asarray(list(words.keys())) == word))])/wscores[list(wordkeys).index(word)])
          
      bgkeys = np.asarray(list(set(list(bigrams.keys())))) 
      
      for bg in bgkeys:
          scores.append(np.median(np.asarray(list(bigrams.values()))[np.where(np.asarray(list(bigrams.keys()) == word))])/wscores[list(bgkeys).index(bg)])
      
      wordkeys = list(wordkeys)
      wordkeys.extend(list(bgkeys))
      
      return wordkeys,MinMaxScaler().fit_transform(scores)