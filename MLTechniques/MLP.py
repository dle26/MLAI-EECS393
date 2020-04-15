#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 00:11:58 2020

@author: anibaljt
"""


from .Technique import Technique

class MLP(Technique):
    
    
    GENERAL_USE = True
    
    TECHNIQUE_TYPE = "supervised"
    
    def __init__(self):
        self.model = None
 
    def get_class_name():
        return 'MLP'
    
    def get_name():
        return 'multilayer perceptron'

    def get_category():
        return 'mlp'
    
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
    