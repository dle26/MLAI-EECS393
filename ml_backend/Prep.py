#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:44:58 2020

@author: anibaljt
"""

from Data import DATA
import numpy as np
import scipy as sp
import nltk
import cv2


class DATAPREP:
    
    def __init__(self):
        self.data = DATA()
    
    '''Will  make the intial data file here w/ json data received from frontend 
    and perform eval + structural analysis
    
    For stat analysis, handle directories as a single "entitiy", calculate average
    
    '''


    ''' need skip gram for this'''
    
    def process_data(self):
        return self.data
    
    

    def eval_data(self):

        #### evaluate curse of dimensionality
        #### extreme sparsity
        #### extremely small
        #### extreme class imbalance
        #### NO USER INPUT

        return -1
    
    
    def data_features(self):
        
          
        #### calculate nan-sparsity
        #### calculate zero sparsity
        ### add together?
        #### index/column ratio
        #### total dimensionality 
        
        return -1
    
    
    
    def sparsity(self,checknan=True):
        pass
    
    
    
    
    
    
    
    
    
    
    
        
    
        