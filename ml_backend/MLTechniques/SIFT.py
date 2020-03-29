#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 02:02:49 2020

@author: anibaljt
"""

import cyvlfeat as vlfeat
import numpy as  np

class SIFT:
    
    TECHNIQUE_TYPE = "preprocessing"
    
    def __init__(self):
      self.model = None
        
    def train(self,data):
        
        train_data = data.data
        sift_vectors = []
        
        if data.multi_channel_image:
            #### functionality for multiple channels
            for num,array in enumerate(train_data):
                data[num] = np.reshape(array,data.dimension[0],data.dimension[1])
            

    
    def predict(self):
        pass
    
    
    def get_model(self):
        return self.model
    
    def set_model(self,model):
        self.model = model
    

