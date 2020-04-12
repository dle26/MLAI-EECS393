#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: 

Standardization class for Results collection/model eval

"""

from sklearn import metrics
import copy 
import numpy as np


class INTERPRET:
    
    
    def __init__(self,data,performance_threshold=0.6):
        
        self.data = copy.deepcopy(data)
        self.performance_threshold = performance_threshold

        
    def interpret(self):
        
        if self.data.analysis_type == 'supervised':
            self.data = self.supervised_accuracy_metrics()
        
            if self.data.feature_importances != []:
                self.data = self.fi_interpret()
        else:
            self.data = self.uns_accuracy_metrics()
        
        return self.data
    
    
    def supervised_accuracy_metrics(self):
        
        techniques = self.data.techniques

        all_results = {}
        
        ## TODO: run for all techniques - currently just 1
        for n,tech in enumerate([techniques[-1]]):
            
            int_results = {}
            
            preds = np.asarray(self.data.prediction_results[n])
            true_labels = np.asarray(self.data.test_labels[n])

            int_results["Accuracy"] = metrics.accuracy_score(true_labels,preds)
            int_results['F1 Score'] = metrics.f1_score(true_labels,preds,average='macro')
            int_results["Confusion Matrix"] = metrics.confusion_matrix(true_labels, preds)
            # int_results["NL Results"] = self.NLResults()
            
            all_results[tech] = int_results
        all_results['best'] = self.assign_top_model_sup(all_results)
        all_results['analysis type'] = 'supervised'
        self.data.interpreted_results = all_results
        print(self.data.interpreted_results)
        return self.data
            
 
    def uns_accuracy_metrics(self):
           
        techniques = self.data.techniques

        all_results = {}
        
        ## TODO: run for all techniques - currently just 1
        ### TODO: add more eval methods??
        
        for n,tech in enumerate([techniques[-1]]):
            
            int_results = {}
            
            preds = np.asarray(self.data.prediction_results[n])

            int_results["Silhouette"] = metrics.silhouette_score(self.data.test_data,preds)
            int_results['CH Score'] = metrics.calinski_harabasz_score(self.data.test_data,preds)
            int_results["NL Results"] = self.NLResults()

            
            all_results[tech] = int_results
            
        '''ALLRESULTS - a dict of dicts which will be returned to frontend '''
        all_results['best'] = self.assign_top_model_unsup(all_results)
        all_results['analysis type'] = 'unsupervised'
        
        self.data.interpreted_results = all_results

        return self.data
    
    
    
    def fi_interpret(self):
        return self.data
    
    
    def NL_results(self,name):
        pass
    
    
    def assign_top_model_sup(self,class_results):
        
        best_technique = None
        highest_F1 = 0
        
        for technique in class_results.keys():
            
            # self.update_result_tup(technique,class_results[technique]["F1 Score"])
          
          if class_results[technique]["F1 Score"] > highest_F1:
                highest_F1 = class_results[technique]["F1 Score"]
                best_technique = technique
                
          if class_results[technique]["F1 Score"] == highest_F1:
              if class_results[technique]["Accuracy"] < class_results[best_technique]["Accuracy"]:
                    best_technique = technique
                        
              elif class_results[technique]["Accuracy"] == class_results[best_technique]["Accuracy"]:
                  if np.random.randint(0,2) > 0:
                       best_technique = technique

        self.data.best_model = (best_technique,class_results[best_technique]["F1 Score"])
        return best_technique
    
    
    def assign_top_model_unsup(self,class_results):
        
        best_technique = None
        highest_sil = 0
        
        for technique in class_results.keys():
            
          self.update_result_tup(technique,class_results[technique]["Silhouette"])
          
          if class_results[technique]["Silhouette"] > highest_sil:
                highest_sil = class_results[technique]["Silhouette"]
                best_technique = technique
                
          if class_results[technique]["Silhouette"] == highest_sil:
              if class_results[technique]["CH Score"] < class_results[best_technique]["Accuracy"]:
                    best_technique = technique
                        
              elif class_results[technique]["CH Score"] == class_results[best_technique]["CH Score"]:
                  if np.random.randint(0,2) > 0:
                       best_technique = technique

        self.data.best_model = (best_technique,class_results[best_technique]["Silhouette"])
        return best_technique
        
    
    
    ''' BIG TODO HERE '''
    def update_result_tup(self,technique,score):
        
         for n,tup in enumerate(self.data.data_for_update):
             
             if technique in tup:
                ml_update = list(self.data.data_for_update[n])
                ml_update.append(score)
                self.data.data_for_update[n] = tuple(ml_update)
                
         return -1 
