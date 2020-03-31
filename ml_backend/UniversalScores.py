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
        
        boost_ppr,scores_ppr = UniversalScores.initialize('preprocessing')

        results,values,matched_words = UniversalScores.compare_keywords(scores,boost,keywords)
        
        results = UniversalScores.weighted_select(results)
        
        ppr_results = []
        ppr_matches = []
        
        for approach in results:
            results,values,matches = UniversalScores.compare_keywords(scores_ppr,boost_ppr,keywords,approach)
            ppr_results.append(results.index(values.index(max(values))))
            ppr_matches.append(matches)
    
    
        return results,ppr_results,matches,ppr_matches
    
    
    ### TODO!!!!!!!
    
    def apply_skipgram(self):
        pass
    
    
    def weighted_select(self,keywords,scores):
        
        scores = np.asarray(list(scores.values()))
        indicies = np.choice(len(keywords),3,scores/np.sum(scores))
        return np.asarray(keywords)[indicies],scores[indicies]
        
    
    ### REDOTHIS FOR PICKLE FILES!!
    
    def initialize(type_identifier):
        
        if os.path.exists('BOOST.pkl'):
            boost = pickle.load(open('BOOST.pkl','rb'))
        else:
            boost = {"supervised":{},"unsupervised":{},"preprocessing":{}}
        
        
        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
                if obj.TECHNIQUE_TYPE == type_identifier and obj.TECHNIQUE_TYPE not in boost:
                     boost[type_identifier][obj.get_name()] = {}
        
        pickle.dump(boost,open("BOOST.pkl","wb"))
        
        return boost[type_identifier],pickle.load(open('TECHNIQUE_SCORES.pkl','rb'))[type_identifier]
        
        
    

    def key_sort(keys,values): 
  
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
    
    

    def compare_keywords(scores,boost,keywords,approach):
        
        #### which techniques correspond to which words? - need adagram here!!!!
        technique_matches = {}
        match_percentage = {}

        for dic in (scores,boost):
            for technique in dic:
                num_matches = 0
                technique_matches[technique] = {}
                matched_words = []
                
                for keyword in dic[technique].keys():
                    if keyword in keywords:
                        technique_matches[technique][keyword] = dic[technique][keyword][1]
                        if approach != None:
                          if keyword in approach:
                            technique_matches[technique][keyword] = (dic[technique][keyword][1]+dic[technique][keyword][1]*0.1)
                        num_matches += 1
                        matched_words.append(keyword)
                        
                match_percentage[technique] = num_matches/len(keywords)
                matched_words[technique] = matched_words
                
            for scoreset in technique_matches.values():
                technique_matches[technique] = np.average([sum(list(scoreset)),match_percentage[technique]],weights=[0.75,0.25])
    
        results,values = UniversalScores.key_sort(list(technique_matches.keys()),list(technique_matches.values()))
        
        return results,values,matched_words    