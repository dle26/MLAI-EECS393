#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt

"""

import numpy as np
import copy
import inspect
import SMLTechniques
import UMLTechniques
import PreProcessing


class SelectionAgent:
    
    def __init__(self,data,mining_threshold):
        
        self.data = copy.deepcopy(data)
        self.mining_threshold
        
        
    def selectAnalysisApproach(self,time_constraint,no_labels=False):
        
        if no_labels:
           mltechniques,preprocessing = self.getMethods(unsupervised=True)
        else:
             mltechniques,preprocessing = self.getMethods()
             
        preprocessing_ml_scores = {}
        input_ml_scores = {}
        scores = {}
        
        user_input = self.data.get_information()
        
        for key,keywords in mltechniques.items():  
            if 'custom' not in list(keywords.keys()):
               score = self.score_user(keywords,user_input)
               input_ml_scores[key] = keywords
               scores[key] = score
               
        if max(list(scores.values())) < self.threshold:
            results = TextSelect(self.data).selectAnalysisApproach(time_constraint,no_labels)
        else:
            results = self.weighted_select(input_ml_scores,scores,time_constraint)
        
        for tup in results:
          if 'custom' not in tup[0]:
            for key2,procscores in preprocessing.items():
               preprocessing_ml_scores[(key2,key)] = self.score_ml_proc(tup[1],procscores)
               
        self.data.set_techniques(self.weighted_preproc_select(preprocessing_ml_scores,time_constraint))

        return self.data
        
        

    def getMethods(self,unsupervised=False):
        
        all_classes = {}
        if unsupervised:
             for name, obj in inspect.getmembers(UMLTechniques):
                 if inspect.isclass(obj):
                     all_classes[str(name)] = obj.keywords
        else:    
            for name, obj in inspect.getmembers(SMLTechniques):
                if inspect.isclass(obj):
                    all_classes[str(name)] = obj.keywords
        
        all_preprocessing = {}
        for name, obj in inspect.getmembers(PreProcessing):
            if inspect.isclass(obj):
                all_preprocessing[str(name)] = obj.keywords

        return all_classes,all_preprocessing


    def score_user(self,keywords,usinput):
        
        #### TODO: augment with ada skip gram
        score = 0
        for word in usinput:
            if word in list(keywords.keys()):
                score += keywords[word]
        return score
        
    def apply_asg(self):
        pass
    
    def score_ml_proc(self,words,words2):
        
        score = 0
        for word in words.keys():
            if word in list(words2.keys()):
                score += min([words[word],words2[word]])
                
        return score
        
    
    def weghted_preproc_select(self,scores,time_constraint):
              
        if time_constraint == 0:
            
            return np.asarray(list(scores.keys()))[np.choice(len(scores),1,scores/np.sum(list(scores).values()))]
        else:
            return np.asarray(list(scores.keys()))[np.choice(len(scores),3,scores/np.sum(list(scores).values()))]
        

        
    
    def weighted_ml_select(self,keywords,scores,time_constraint):
        
        scores = np.asarray(list(scores.values()))
        
        if time_constraint == 0:
            return np.asarray(list(keywords.items()))[np.choice(len(keywords),1,scores/np.sum(scores))]
        else:
            return np.asarray(list(keywords.items()))[np.choice(len(keywords),3,scores/np.sum(scores))]
        

    
class TextSelect:
    pass
    
'''    
    
        score = 0
        
        if not user:
            return len(list(set(words) & set(words2)))/len(words2)

        for word in words2:
           if word in words.keys():
              score += words[word]
                    
        score /+ words['maxscore']
        ### TODO: optimize experimentally
        if score['numpapers'] > 1:
            score += 0.05
            
        return score
    
'''
