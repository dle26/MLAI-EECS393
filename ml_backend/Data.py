#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 17:30:00 2020

@author: anibaljt
"""

import copy


class DATA:
    
    def __init__(self,data,user,labels =None):
        
        self.data = data
        self.labels = labels
        self.user=user
        self.info = None
        self.bestmodel = None
        self.techniques = []
        self.stat_info = None
        self.prior_models = []
        self.preprocessed_data = None
        self.results = []
        self.time_constraint = None
        self.feature_importances = None
        self.prediction_results = None
        self.prior_preprocessing = []
        
    def get_data(self):
        return copy.deepcopy(self.data) 
    
    def get_time(self):
        return self.time_constraint
    
    def set_time(self,time):
        self.time_constraint = time

    def get_preprocesseddata(self):
        if self.preprocessed_data != None:
            return copy.deepcopy(self.preprocessed_data)
        return None
    
    def set_preprocesseddata(self,pdata):
        self.preprocessed_data = pdata
    
    def get_user(self):
        return self.user
    
    def get_info(self):
        return self.info
    
    def add_info(self,desc):
        self.info.extend(desc)
    
    def get_models(self):
        return self.models
    
    def add_model(self,model):
        self.models.extend(model)
        
    def get_best_model(self):
        return self.bestmodel
        
    def set_best_model(self,best):
        self.bestmodel = best
        
    def get_techniques(self):
        return self.techniques
    
    def set_techniques(self,tech):
        self.techniques.extend(tech)
        
    def get_labels(self):
        return self.labels
    
    def get_stat_info(self):
        return self.stat_info
    
    def set_stat_info(self,stats):
        self.stat_info = stats
        
    def get_prior_models(self):
        return self.prior_models
        
    def set_prior_model(self,prior_model,name):
        self.prior_models[name] = prior_model
    
    def get_results(self):
        return self.results
    
    def add_results(self,res,name):
        self.results[name] = res
    
    def add_feat_importances(self,fi,name):
        self.feature_importances[name] = fi
    
    def add_pred_results(self,results):
        self.prediction_results.extend(results)
        
    def add_prior_preprocessing(self,prior_pre,name):
        self.prior_preprocessing[name] = prior_pre
    
    def get_prior_preprocessing(self):
        return self.prior_preprocessing 
        
        
