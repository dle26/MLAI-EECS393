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
import pandas as pd
import itertools

class DATAPREP:
    
    def __init__(self):
        self.data = DATA()
    
    '''Will  make the intial data file here w/ json data received from frontend 
    and perform eval + structural analysis
    
    For stat analysis, handle directories as a single "entity", calculate average
    
    '''

    ''' PRIORITY: need ada skip gram for this!!!! '''
    

    def process_data(self):
        return self.data
    

    ### TODO: add in text data handling + unsupervised learning  
    def eval_text_data(self):
        pass
    
    
    def eval_data(self,multifile = False):
        
        
        #### need text=False
        score = 1
        
        if self.data.user_input == None: 
            score -= 0.05
        
        
        if multifile == False:
            if np.count_nonzero(np.isnan(self.data.get_data()))/len(self.data) > 0.5:
                score -= 0.1
            oratio = self.outlier_ratio(self.data.get_data())
            
        else:
            if self.get_sparsity() > 0.5:
                score -= 0.1

            oratio = 0
            for num,i in enumerate(self.data.get_data()):
                oratio += self.outlier_ratio(self.data[i])
                
        if (oratio/num) > 0.1:
                score -= 0.1

                
        if len(self.data.labels) < 25:
            score -= 0.25
            
        if self.get_label_ratios() > (1/len(set(self.data.get_labels())))/2:
            score -= 0.1
      
        self.data = self.data_features()
        
        return score
    
    
    def eval_without_labels(self):
        pass 
    
    
    def data_features(self):
        
        ### WHAT GOES HERE??

        # - sparsity
        # - multiclass
        # - outliers
        # - dimensionality 
        
        #### COMBINE WITH USER TERMS TO GET SEARCH TERMS
        ####  bigrams 'i.e. "images sparse" or "handwritten outliers"
        #### sciencedirect searching is just by terms, NOT by context
        
        user_input = self.data.get_info().copy()
 
        return -1
    
    
    def get_label_ratios(self):
        
        leng = len(self.data.get_labels())
        lst = list(self.data.get_labels())
        
        ratios = []
        
        for i in np.unique(self.data.get_labels()):
            ratios.append(lst.count(i)/leng)
            
        return np.std(ratios)
    
    
    
    def get_sparsity(self):
        
        data = self.data.get_data()
        sparsity = 0
        
        for file in data:
            sparsity += np.count_nonzero(np.isnan(data[file]))/len(data[file])
        
        return sparsity/len(data)
    
    

    def extract_labels(self):
        pass
    
    
    
    def text_eval(self):
        pass
    
    
    
    def format_images(self):
        pass
    

    
    def outlier_ratio(self,data):
        
        data = pd.DataFrame(data)
        outlier_ratio = 0
        
        for i in data.columns:
            mean = np.mean(data[i])
            std = np.std(data[i])
            vals = (data[i].values-mean)/std
            outlier_ratio /= len(np.where(np.abs(vals) > 3)[0])/len(data[i])
        
        return outlier_ratio
    
    
    def generate_combinations(self,l1,l2):
        
        combinations = []
        permutations = itertools.permutations(l1, 2)
        for perm in permutations:
            zipped = zip(perm, l2)
            combinations.append(list(zipped))
        return combinations
    
    
    
    
    
    
    