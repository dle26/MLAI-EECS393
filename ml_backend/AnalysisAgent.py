#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt
"""

import copy 
import SMLTechniques
import UMLTechniques
import PreProcessing
import inspect
import numpy as np


class AnalysisAgent:
    
    def __init__(self,data):
        
        self.data = copy.deepcopy(data)
        
        
    def usePriorModels(self):
        
      for i in range(len(self.data.prior_preprocessing)):
          
        preprocessed_data = self.data.prior_preprocessing[i].get_model().apply_technique(self.data)
        self.data.prior_models[i].predict(self.data,preprocessed_data,self.data.prior_models[i].get_model())

      return self.data
     
        
    def fitApproaches(self,unsupervised=False):
        
        preprocessing_package = list(np.asarray(inspect.getmembers(PreProcessing)).flatten())
        if unsupervised:
            ml_package = list(np.asarray(inspect.getmembers(UMLTechniques)).flatten())
        else:
            ml_package = list(np.asarray(inspect.getmembers(SMLTechniques)).flatten())
            
        for technique in self.data.techniques:
    
            obj = preprocessing_package[preprocessing_package.index(technique+1)]
            self.data = obj().train(self.data)
            mlmodel = ml_package[ml_package.index(technique+1)]
            self.data = mlmodel().train(self.data)
        
        return self.data