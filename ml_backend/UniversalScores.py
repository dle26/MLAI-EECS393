#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:25:59 2020

@author: anibaljt
""" 

import inspect
import numpy as np
import MLTechniques
import pickle
import os

class UniversalScores:
    
    
    def reference(keywords,type_indentifier='supervised',top_approaches=None):

        if (type_indentifier == 'supervised'): 
           boost,scores = UniversalScores.initialize('supervised')
            
        if (type_indentifier=='unsupervised'): 
            boost,scores = UniversalScores.initialize('unsupervised')
        

        results,values,matched_words = UniversalScores.compare_keywords(scores,boost,keywords)
        if np.sum(values) > 0:
            results = UniversalScores.weighted_select(results,values)
        

        return results,matched_words
    
    
    ### TODO!!!!!!!
    
    def apply_skipgram():
        pass
    
    
    def weighted_select(keywords,scores):
        
        scores = np.asarray(scores)
        indicies = np.random.choice(len(keywords),2,scores/np.sum(scores))
        return np.asarray(keywords)[indicies],scores[indicies]
        

    
    def initialize(type_identifier):
        
        if os.path.exists('BOOST.pkl'):
            boost = pickle.load(open('BOOST.pkl','rb'))
        else:
            boost = {"supervised":{},"unsupervised":{}}
        
        if os.path.exists('TECHNIQUE_SCORES.pkl'):
            normal = pickle.load(open('TECHNIQUE_SCORES.pkl','rb'))
        else:
            normal = {"supervised":{},"unsupervised":{}}
        
        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
                if obj.TECHNIQUE_TYPE == type_identifier and (obj.get_name() not in boost[type_identifier] and obj.get_name() not in normal[type_identifier]):
                     boost[type_identifier][obj.get_name()] = {}
        
        pickle.dump(boost,open("BOOST.pkl","wb"))
        pickle.dump(normal,open("TECHNIQUE_SCORES.pkl","wb"))
        
        return boost[type_identifier],normal[type_identifier]
        
        
    
    def key_sort(keys,values): 
      if len(list(values)) > 0:
        for i in range(1, len(values)): 
            
            key = values[i] 
            key2 = keys[i]
            
            j = i-1
            while j >=0 and key < values[j] : 
                values[j+1] = values[j] 
                keys[j+1] = values[j]
                j -= 1
            values[j+1] = key 
            keys[j+1] = key2
            
      return keys,values
    
    

    def compare_keywords(scores,boost,keywords):
        
        #### which techniques correspond to which words? - need adagram here!!!!
        technique_matches = {}
        match_percentage = {}
        matches = []

        for dic in (scores,boost):
            for technique in dic:
                num_matches = 0
                technique_matches[technique] = []
                matched_words = []
                
                for keyword in dic[technique].keys():
                    if keyword in keywords:
                        technique_matches[technique][keyword] = dic[technique][keyword][1]
                        num_matches += 1
                        matched_words.append(keyword)
                        
                match_percentage[technique] = num_matches/len(keywords)
                matches.append(matched_words)
     
            for scoreset in list(technique_matches.values()):
                technique_matches[technique] = np.average([sum(list(scoreset)),match_percentage[technique]],weights=[0.75,0.25])
    
        results,values = UniversalScores.key_sort(list(technique_matches.keys()),list(technique_matches.values()))

        return results,values,matches  
    
    
    
    def select_from_usage(names,number,analysis_type):
        
        techniques = []
        
        if os.path.exists('BOOST.pkl'):

            boost = pickle.load(open('BOOST.pkl','rb'))
        else:
            boost = {}
        
        if os.path.exists('TECHNIQUE_SCORES.pkl'):
            normal = pickle.load(open('TECHNIQUE_SCORES.pkl','rb'))
        else:
             normal = {}
        

        all_scores = []
        for name in names:
            name_score = []
            name_uses = []
            found = False
            for tup in boost[analysis_type][name]:
                if tup[0] == name:
                   name_score.append(tup[1])
                   name_uses.append(tup[2])
            if len(name_score) > 0:
                ### WEIGHTS scores based on num uses + presence in boost
                #### ADD IN "GENERAL" facet to scoring??
                
                all_scores.append((np.median(name_score)+np.median(np.array(name_uses)/np.sum(name_uses))*1)+0.1) ###adjust the weights (currently 1/0.1) as needed 
                found = True
            name_score = []
            name_uses = []
            
            if name in normal[analysis_type].keys():
              for tup in normal[analysis_type][name]:
                if tup[0] == name:
                   name_score.append(tup[1])
                   name_uses.append(tup[2])
                   
            if len(name_score) > 0:  
              all_scores.append((np.median(name_score)+np.median(np.array(name_uses)/np.sum(name_uses))*1))
            elif len(name_score) == 0 and not found:
                all_scores.append(0)
   
        if np.sum(all_scores) == 0: #### arbitrary threshold for handling very sparse info (early uses) - optimize this
            all_scores = None
        else:
            all_scores = np.array(all_scores)/np.sum(all_scores)
            
        techniques.append(np.random.choice(names,number,p=all_scores))

        return list(np.ravel(np.asarray(techniques)))
        
    
