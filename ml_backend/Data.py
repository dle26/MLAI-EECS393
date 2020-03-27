#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 17:30:00 2020

@author: anibaljt
"""

import copy


class DATA:
    
    def __init__(self):
        
        self.data = None
        self.labels = None
        self.user= None
        self.info = None
        self.bestmodel = None
        self.techniques = []
        self.stat_info = None
        self.prior_models = []
        self.preprocessed_data = None
        self.results = None
        self.time_constraint = None
        self.feature_importances = None
        self.prediction_results = None
        self.prior_preprocessing = []
        self.matching_keywords = {"Preprocessing": [], "ML":[]}
        
    
    
    
    ####  GENERAL USE
    def get_data(self):
        return copy.deepcopy(self.data) 
    
    def get_time(self):
        return self.time_constraint
    
    def set_time(self,time):
        self.time_constraint = time
      
    def add_info(self,desc):
        self.info.extend(desc)
        
    def get_labels(self):
        return self.labels
    
       
        
    ### USE IN SELECTIONAGENT
    def get_info(self):
        return self.info
    
    def set_techniques(self,tech):
        self.techniques.extend(tech)
    
    def set_preprocessing_techniques(self):
        return self.techniques
        
    def set_matching_keywords(self,value,ml=True):
        if ml:
            self.matching_keywords["ML"] = value
            return
        self.matching_keywords["Preprocessing"] = value
    


    #### USE IN ANALYSISAGENT
    def get_preprocessed_data(self):
        if self.preprocessed_data != None:
            return copy.deepcopy(self.preprocessed_data)
        return None
    
    def set_preprocessed_data(self,pdata):
        self.preprocessed_data = pdata

    def add_model(self,model):
        self.models.extend(model)
    
    def get_prior_models(self):
        return self.prior_models
    
    def add_feat_importances(self,fi,name):
        self.feature_importances[name] = fi
        
    def get_feat_importances(self):
        return self.feature_importances
        
    def add_pred_results(self,results):
        self.prediction_results.extend(results)
    
    def get_prior_preprocessing(self):
        return self.prior_preprocessing 
    
    
    
    
    ### USE IN INTERPRETATION AGENT
    def get_best_model(self):
        return self.bestmodel
        
    def set_best_model(self,best):
        self.bestmodel = best
        
    def get_techniques(self):
        return self.techniques
         
    def get_preprocessing_techniques(self):
        return self.techniques
    
    def add_interpreted_results(self,res):
        self.results = res
    
    def get_pred_results(self):
       return self.prediction_results
   
    def get_matching_keywords(self):
        return self.matching_keywords
    
    
    
    
    #### USE IN REUSE AGENT 
    def get_models(self):
        return self.models

    def get_user(self):
        return self.user
    



    ####OTHER - TBD
    def set_prior_model(self,prior_model,name):
        self.prior_models[name] = prior_model
    
    def get_interpreted_results(self):
        return self.results
    
    def add_prior_preprocessing(self,prior_pre,name):
        self.prior_preprocessing[name] = prior_pre
    

        
        
