#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 17:25:33 2020

@author: anibaljt
"""

import abc

class Technique(abc.ABC):
    
       
    @abc.abstractmethod
    
    def static_get_keywords():
        
        pass
    
    
    @abc.abstractmethod
    
    def get_name(self):
        
        pass
    
    
    @abc.abstractmethod
    
    def apply_technique(self):
        
        pass
    
    
    
    
    