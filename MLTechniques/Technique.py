#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt

Abstract class for ensuring ML techniques in package are properly structured
"""

import abc

class Technique(abc.ABC):

    TECHNIQUE_TYPE = None
    ISDEEP = None
    
    @abc.abstractmethod
    def get_website():
        pass
    
    @abc.abstractmethod
    def preprocess(data):
        pass  
    
    @abc.abstractmethod
    def get_category():
        pass
        
    @abc.abstractmethod
    def get_name():
        pass
    
    @abc.abstractmethod
    def get_class_name():
        pass
    
    @abc.abstractmethod
    def train(data):
        pass
