#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt
"""

import abc

class Technique(abc.ABC):
       
    @abc.abstractmethod
    
    def static_get_keywords():
        pass
    
    
    @abc.abstractmethod
    
    def get_name():
        pass
    
    
    @abc.abstractmethod
    
    def train(self):
        pass
    
    
    @abc.abstractmethod
    
    def predict(self):
        pass
    
    
    @abc.abstractmethod

    def set_model(self):
        pass
    
    @abc.abstractmethod
    
    def get_model(self):
        pass
