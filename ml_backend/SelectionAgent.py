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
from TextMine import TEXTMINE


class SELECT:
    
    def __init__(self,data,threshold,techkey):
        
        self.data = copy.deepcopy(data)
        self.mining_threshold = threshold
        self.technical_keywords = techkey
        
        
    def selectAnalysisApproach(self,time_constraint,no_labels=False):
        
        if no_labels:
           mltechniques,preprocessing = self.getMethods(unsupervised=True)
        else:
            mltechniques,preprocessing = self.getMethods()
             
        preprocessing_ml_scores = {}
        input_ml_scores = {}
        scores = {}
        
        user_input = self.data.get_info()
        scores,input_ml_scores = self.get_initial_scores(mltechniques,user_input)
        if max(list(scores.values())) < self.mining_threshold:
            textmine = TEXTMINE(self.data,self.technical_keywords)
            user_input = textmine.from_database()
            scores,input_ml_scores = self.get_initial_scores(mltechniques,user_input)
            
        else:
            results = self.weighted_select(input_ml_scores,scores,time_constraint)
        
        for tup in results:
          if 'custom' not in tup[1]:
            for key2,procscores in preprocessing.items():
               preprocessing_ml_scores[(tup[0],key2)] = self.score_ml_proc(tup[0],procscores)
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
                self.data.set_matching_keywords(word)
        return score
        
    
    def apply_asg(self):
        ## TODO WHEN ALEC IS DONE
        pass
    
    
    def score_ml_proc(self,words,words2):
        
        score = 0
        for word in words.keys():
            if word in list(words2.keys()):
                score += min([words[word],words2[word]])
                self.data.set_matching_keywords(word)
                self.data.set_matching_keywords(word,False)
                
        return score
        
    
    def weghted_preproc_select(self,scores,time_constraint):
            return np.asarray(list(scores.keys()))[np.choice(len(scores),1,scores/np.sum(list(scores).values()))]
        

    def weighted_ml_select(self,keywords,scores,time_constraint):
        
        scores = np.asarray(list(scores.values()))
        
        if time_constraint == 0:
            return np.asarray(list(keywords.items()))[np.choice(len(keywords),1,scores/np.sum(scores))]
        else:
            return np.asarray(list(keywords.items()))[np.choice(len(keywords),3,scores/np.sum(scores))]
    
    
    def get_initial_scores(self,techniques,user_input):
        
        scores = {}
        input_ml_scores = {}
        
        for key,keywords in techniques.items():  
               score = self.score_user(keywords,user_input)
               input_ml_scores[key] = keywords
               scores[key] = score
               
        return input_ml_scores,scores
        