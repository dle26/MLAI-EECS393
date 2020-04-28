#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:19:49 2020

@author: anibaljt
"""

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
import json
import inspect
import numpy as np
import os
import MLTechniques
from .TextProcess import TEXTPROCESS
import requests
import copy


class TEXTMINE:
    
    def __init__(self,queries,user_keywords,user_id,analysis_type):
        
        self.queries = queries
        self.user_keywords = user_keywords
        self.user_id = user_id
        self.analysis_type = analysis_type

        
    def from_database(self,time_constraint):
 
        con_file = open("config.json")
        config = json.load(con_file)
        con_file.close()
        client = ElsClient(config['apikey'])
        ###TODO: add year back in??
        searchwords = {'category':[],'specific':[]}
        
        if self.analysis_type == 'supervised':
            tech_words = ["machine learning"]
            
        elif self.analysis_type == 'unsupervised': 
             tech_words = ["clustering"]

        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
                if obj.TECHNIQUE_TYPE == self.analysis_type:
                    if not obj.ISDEEP or time_constraint > 1:
                        searchwords['specific'].append(obj.get_name())
                        searchwords['category'].append(obj.get_category())

        print(searchwords['category'])
        textmine_results = {'words':[],'scores':[],'allwords':[]}


        print("-----UNKNOWN DATA DETECTED: INITIATING TEXT MINING-----")
        print()
        allurls = []
        
        combos = self.generate_combinations(self.queries,tech_words)

        if time_constraint == 1:
            query_size = set_query_number(combos,100)
        if time_constraint == 2:
            query_size = set_query_number(combos,250)
        if time_constraint == 3:
            query_size = set_query_number(combos,500)
        if time_constraint == 4:
            query_size = set_query_number(combos,750)
        if time_constraint == 5:
            query_size = set_query_number(combos,1000)
    
        i = 0
        for n,combo in enumerate(combos):
             print("SEARCH QUERY " + str(n+1) + ":")
             print(combo)
             print()
            
             string = ""
             for word in combo:
                 string += (word + " ") 
                 
             doc_srch = ElsSearch(string, 'sciencedirect')
             results = TEXTMINE.execute_modified(doc_srch.uri,client,get_all=True,set_limit=query_size)
             
             if results != 0:
               print("SUCCESSFUL QUERY")
               for num,res in enumerate(results):
                 
                 DOI = res['prism:doi']
                 URL = 'https://api.elsevier.com/content/article/DOI/' + str(DOI) + "?APIkey=" + str(config['apikey'])
                 if URL not in allurls:
                 
                     r = requests.get(URL)
                     allurls.append(URL)
                        
                     with open(str(self.user_id),'w') as f:
                        f.write(r.text)
                     f.close()
                 
                     foundwords,allwords = TEXTPROCESS.findkeywords(str(self.user_id),searchwords,self.user_keywords)
                     if len(list(foundwords.keys())):
                        i += 1
                        print(i)
                     textmine_results['words'].extend(list(foundwords.keys()))
                     textmine_results['scores'].extend(list(foundwords.values()))
                     textmine_results['allwords'].extend(allwords)
                     os.remove(str(self.user_id))

        print("------MINING COMPLETE: SEARCHING FOR KEYWORDS-----")
        keywords,keyword_scores = self.adjust_output(textmine_results)
        return keywords,keyword_scores,searchwords
        
 
    ### TODO: CITE ELSAPY - I MODIFIED THE SRC FOR MLAI 
    def execute_modified(uri,els_client = None, get_all = False,set_limit=25):

        api_response = els_client.exec_request(uri)
        
        if api_response['search-results']['opensearch:totalResults'] is None:
                return 0
        
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
        
      return tosort,basis
    
    
    def generate_combinations(self,l1,l2):
        
        l3 = []
        for tup in l1:
           for word in l2:
               t = copy.deepcopy(tup)
               t += (word,)
               l3.append(t)
        return l3
    
    

    def adjust_output(self,words):

      scores = []

      wordkeys = list(set(words['words']))
      
      ''' adjust for total number of occurrences '''
      for word in wordkeys:
          score = np.sum(np.asarray(words['scores'])[np.where(np.asarray(words['words']) == word)])
          scores.append(score)

      return wordkeys,list(np.asarray(scores)/np.sum(scores))



def set_query_number(user_input,target):
        
        number = int(target/len(user_input))
        
        while (number%25 > 0):
            number+=1
        
        return number
