#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 23:45:21 2020

@author: anibaljt
"""

from .Technique import Technique

class RandomForest(Technique):
    
    
    GENERAL_USE = True
    
    TECHNIQUE_TYPE = "supervised"
    
    def __init__(self):
        self.model = None
 
    def get_name():
        return 'random forest'

    def get_category():
        return 'random forest'
    
    def get_general_category():
        return 'machine learning'
    
    def preprocess(self,data):
        pass
        
    def train(self,data,time_constraint):
        pass

    def predict(self,data,labels,model):
        pass
    
    def set_model(self,model):
        self.model = model
    
    
    def get_model(self):
        return self.model
    