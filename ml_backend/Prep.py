#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:44:58 2020

@author: anibaljt
"""

import numpy as np
import scipy as sp
import nltk
import cv2
import pandas as pd
import itertools


class DATA:
    
    def __init__(self):
        
        self.data = None
        
        self.labels = None
        
        self.user= None
        
        self.descriptive_info = []
        
        self.bestmodel = None
        
        self.techniques = []
        
        self.prior_models = []
        
        self.preprocessed_data = None
        
        self.results = None
        
        self.time_constraint = None
        
        self.feature_importances = None
        
        self.prediction_results = None
        
        self.prior_preprocessing = []
        
        self.current_models = []


class DATAPREP:
    
    def __init__(self,multifile=False):
        self.data = DATA()
        self.multifile = False
        

    def process_data(self):
        return self.data
    
    
    ### TODO: add in text data handling + unsupervised learning  
    def eval_text_data(self):
        pass
    
    
    def eval_data(self):
        
        score = 1
        data_features = []
        
        if self.data.user_input == None: 
            score -= 0.05

        if self.multifile == False:
            sparsity = np.count_nonzero(np.isnan(self.data.data))/len(self.data)
            oratio = self.outlier_ratio(self.data.data)
            
        else:
            sparsity  = self.get_sparsity() 
            oratio = 0
            for num,i in enumerate(self.data.data):
                oratio += self.outlier_ratio(self.data.data[i])
                
        if sparsity > 0.1:
            data_features.append("sparse")
            if sparsity > 0.25:
                score -= 0.1
             
        if (oratio/num) > 0.05:
             data_features.append("outliers")
             if (oratio/num) > 0.1:
                score -= 0.1
                       
        if len(self.data.labels) < 100:
            data_features.append("small dataset")
            if len(self.data.labels) < 25:
                score -= 0.25
            
        if len(list(set(self.data.labels))) > 2:
            data_features.append("multiclass")
            
        elif len(list(set(self.data.labels))) == 1:
            data_features.append("binary")
            
        else:
            data_features.append("one-class")
        
         
        if self.get_label_ratios() > (1/len(set(self.data.labels)))/3:
            data_features.append("imbalance")
            if self.get_label_ratios() > (1/len(set(self.data.labels)))/2:
                score -= 0.1
        

        info = self.data.descriptive_info.extend(data_features)
        self.data.descriptive_info = []
        self.data.descriptive_info = list(itertools.combinations(info,2))
        self.data.eval_score = score
        
        return self.data
    
    
    def eval_without_labels(self):
        pass 
    
    
    def get_label_ratios(self):
        
        leng = len(self.data.labels)
        lst = list(self.data.labels)
        
        ratios = []
        
        for i in np.unique(self.data.labels):
            ratios.append(lst.count(i)/leng)
            
        return np.std(ratios)
    
    
    
    def get_sparsity(self):
        
        data = self.data.data
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