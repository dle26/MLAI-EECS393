#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:25:59 2020

@author: anibaljt
""" 

import inspect
import copy
import numpy as np
import MLTechniques

class UniversalScores:
    
    
    TECHNIQUE_SCORES = {"supervised":{},"unsupervised":{},"preprocessing":{}}
    BOOST = {"supervised":{},"unsupervised":{},"preprocessing":{}}
    SML_FIRST_USE = True
    UML_FIRST_USE = True
    PRP_FIRST_USE = True



    def reference(keywords,data_score,type_indentifier='supervised'):

        if (type_indentifier == 'supervised' and UniversalScores.SML_FIRST_USE): 
            UniversalScores.initialize('supervised')
            
        if (type_indentifier=='unsupervised' and UniversalScores.UML_FIRST_USE): 
            UniversalScores.initialize('unsupervised')
        
        if (type_indentifier == 'preprocessing' and UniversalScores.PRP_FIRST_USE): 
            UniversalScores.initialize('preprocessing')
   
    
        #### values, flatten the technique-bigram tups
        boost = copy.deepcopy(UniversalScores.BOOST) 
        tech_scores = copy.deepcopy(UniversalScores.TECHNIQUE_SCORES)
            
        if type_indentifier == 'supervised':
            scores = tech_scores["supervised"]
            boost = boost["supervised"]
        
        elif type_indentifier == "unsupervised":
            scores = tech_scores["unsupervised"]
            boost =  boost["unsupervised"]
            
        else:
            scores = tech_scores["preprocessing"]
            boost =  boost["preprocessing"]
          
        #### which techniques correspond to which words?
        technique_matches = {}
        match_percentage = {}

        for dic in (scores,boost):
            for technique in dic:
                num_matches = 0
                technique_matches[technique] = {}
                matched_words = []
                
                for bigram in dic[technique].keys():
                    if bigram in keywords:
                        technique_matches[technique][bigram] = dic[technique][bigram][1]
                        num_matches += 1
                        matched_words.append(bigram)
                        
                match_percentage[technique] = num_matches/len(keywords)
                matched_words[technique] = matched_words
                
            for scoreset in technique_matches.values():
                technique_matches[technique] = data_score * (np.average([sum(list(scoreset)),match_percentage[technique]],weights=[0.75,0.25]))
    
        results,values = UniversalScores.key_sort(list(technique_matches.keys()),list(technique_matches.values()))
        
        
        if  type_indentifier != 'preprocessing':
            results,values = UniversalScores.weighted_select(results,values)
            words = list(matched_words.values())[len(values)-3:len(values)]
            return results[len(results)-3:len(results)],values[len(values)-3:len(values)],words
        
        results,values = UniversalScores.weighted_select(results,values,True)
        
        return results[-1],values[-1],list(matched_words.values())[-1]
    
    
    
    def apply_skipgram(self):
        ## TODO WHEN ALEC IS DONE
        pass
    
    
    def weighted_select(self,keywords,scores,preprocessing=False):
        
        scores = np.asarray(list(scores.values()))
        
        if preprocessing:
            indicies = np.choice(len(keywords),1,scores/np.sum(scores))
            return np.asarray(keywords)[indicies],scores[indicies]
        else:
            indicies = np.choice(len(keywords),3,scores/np.sum(scores))
            return np.asarray(keywords)[indicies],scores[indicies]
        
    
    def initialize(type_identifier):
        
        ### class inspection
        if type_identifier == 'supervised':
            UniversalScores.SML_FIRST_USE = False
            
        if type_identifier == 'unsupervised':
            UniversalScores.UML_FIRST_USE = False
        
        if type_identifier == 'preprocessing':
            UniversalScores.PRP_FIRST_USE = False

        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
                if obj.technique_type == type_identifier:
                     UniversalScores.TECHNIQUE_SCORES[type_identifier][obj.get_name()] = {}


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