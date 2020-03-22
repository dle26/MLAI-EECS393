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
nltk.download('wordnet')


class TEXTMINE:
    
    def __init__(self,user_keywords,technical_keywords,run_id):
        
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
        
        file = open("TextMineResults-" + str(self.run_id) + ".txt","w")
        
        ''' may need the limit of the mining here '''
        num_entities = 0
        
        for combo in self.generate_combinations(self.user_keywords,self.technical_keywords):
            
             string = combo[0] + " " + combo[1]
             doc_srch = ElsSearch(string,'sciencedirect')
             doc_srch.execute(client,get_all = True)

             for num,res in enumerate(doc_srch.results):
                 
                 DOI = res['prism:doi']
                 URL = 'https://api.elsevier.com/content/article/DOI/' + str(DOI)
                 r = requests.get(url = URL,headers=header)
                 
                 if 'INVALID_INPUT' not in str(r.content):
                     file.write(str(r.content))
                     num_entities +=1 
                     
        file.close()
        
        return self.make_word_dict(file,num_entities)
        
        
    def generate_combinations(self,l1,l2):
        
        combinations = []
        permutations = itertools.permutations(l1, 2)
        for perm in permutations:
            zipped = zip(perm, l2)
            combinations.append(list(zipped))
        return combinations
        
         
    
    def make_word_dict(self,file,num_entities):
        
        stop = list(set(stopwords.words('english')))
        all_text = []
        
        with open(file, 'r') as f:
            for line in f.readlines():
                all_text.append(line)
        
        all_text = list(np.flatten(np.array(all_text)))
        
        all_text = [word.lower() for word in all_text]
        
        str_word = self.generate_pos()
        
        counts = {}
        
        for word in list(set(all_text)):
           if word not in str_word:
               if word not in string.punctuation:
                   if word not in stop:
                       counts[word] = all_text.count(word)/len(num_entities)
        
        return counts
        
        
        
    def generate_pos(self):
        
        words = ""
        for synset in list(wn.all_synsets(wn.VERB)):
            words += str(synset.name())
            
        for synset in list(wn.all_synsets(wn.ADV)):
            words += str(synset.name())
        
        for synset in list(wn.all_synsets(wn.ADJ)):
            words += str(synset.name())
            
        return words
    

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
    
