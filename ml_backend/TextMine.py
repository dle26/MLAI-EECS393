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


class TEXTMINE:
    
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
        
        file = open("TextMineResults.txt","w")
        
        ''' may need to limit of the mining here '''
        
        for combo in self.generate_combinations(self.user_keywords,self.technical_keywords):
            
             string = combo[0] + " " + combo[1]
             doc_srch = ElsSearch(string,'sciencedirect')
             doc_srch.execute_modified(doc_srch.uri,client,get_all=True,set_limit=75,get_all = True)

             for num,res in enumerate(doc_srch.results):
                 
                 DOI = res['prism:doi']
                 URL = 'https://api.elsevier.com/content/article/DOI/' + str(DOI) + '?view=META_ABS'
                 r = requests.get(url = URL,headers=header)
                 
                 if 'INVALID_INPUT' not in str(r.content):
                     file.write(str(r.content))
                     
        file.close()
        return self.make_word_dict(file)
        
        
    def generate_combinations(self,l1,l2):
        
        combinations = []
        permutations = itertools.permutations(l1, 2)
        for perm in permutations:
            zipped = zip(perm, l2)
            combinations.append(list(zipped))
        return combinations
        
             
    def make_word_dict(self,file):
        
        ### FROM GOOGLE'S 1T WORD CORPUS - 10K MOST FREQUENT WORDS
        stop = pickle.load(open('stop.pkl','rb'))
        all_text = []
        
        with open(file, 'r') as f:
            for line in f.readlines():
                all_text.append(line)
                
        os.remove(file)
        
        str_word = self.generate_pos()
        
        all_text = list(np.flatten(np.array(all_text)))
        
        all_text = [word.lower() for word in all_text if word.lower() not in str_word
                    and word.lower() not in stop and (word not in string.punctuation or word == '-')]
        
        counts = []
        
        for word in list(set(all_text)):
            counts.append(self.modified_count(200,all_text,word)) 
            
        return self.two_list_sort(list(set(all_text)),counts)[int(len(counts)*0.9):len(counts)]
        
    
    def modified_count(self,length,words,word):
        
        total = 0 
        tracker = 0
        
        for i in range(int(len(words)/length)):
            if word in words[tracker:length]:
                total += 1
            tracker += length
            
        return total/i
            

    def generate_pos(self):
        
        words = ""
        for synset in list(wn.all_synsets(wn.VERB)):
            words += str(synset.name())
            
        for synset in list(wn.all_synsets(wn.ADV)):
            words += str(synset.name())
        
        for synset in list(wn.all_synsets(wn.ADJ)):
            words += str(synset.name())
            
        return words
    
    
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
     
    def format_keywords(self):
       pass
    
