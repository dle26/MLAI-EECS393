#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 00:43:56 2020

@author: anibaljt
"""


from .Technique import Technique

class LSTM(Technique):
    
    
    GENERAL_USE = False
    
    TECHNIQUE_TYPE = "supervised"
    
    def __init__(self):
        self.model = None
 
    def get_name():
        return 'lstm'

    def get_category():
        return 'rnn'
    
    def get_general_category():
        return 'deep learning'
    
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
    