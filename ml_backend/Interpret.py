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
            return self.supervised_accuracy_metrics()
        
        return self.uns_accuracy_metrics()
        

    
    def supervised_accuracy_metrics(self):
        
        techniques = self.data.techniques
        all_results = {}
        
        ## TODO: run for all techniques - currently just 1
        for n,tech in enumerate([techniques[-1]]):
            int_results = {}
            if self.data.prior_test_data is not None:
                int_results['samples'] = self.data.prior_test_indicies
                int_results['results'] = self.data.blind_prediction_results[n]
            else:
                int_results['samples'] = None
                int_results['results'] = None
 
            preds = np.asarray(self.data.prediction_results[n])
            true_labels = np.asarray(self.data.test_labels[n])

            if self.data.feature_importances[n] is not None:
                int_results["Feature Importances"] = self.fi_interpret(self.data.feature_importances[n])
            else:
                int_results["Feature Importances"] = None
            
            int_results["Accuracy"] = metrics.accuracy_score(true_labels,preds)
            int_results['F1 Score'] = metrics.f1_score(true_labels,preds,average='macro')
            int_results["Confusion Matrix"] = metrics.confusion_matrix(true_labels, preds)
            # int_results["NL Results"] = self.NLResults()
            
            all_results[tech] = int_results
        all_results['best'] = self.assign_top_model_sup(all_results)
        all_results['analysis type'] = 'supervised'
        all_results['education'] = self.data.educational_info
        self.data.interpreted_results = all_results
        return self.data
            
 
    def uns_accuracy_metrics(self):
           
        techniques = self.data.techniques

        all_results = {}
        
        ## TODO: run for all techniques - currently just 1
        ### TODO: add more eval methods??
        
        for n,tech in enumerate([techniques[-1]]):
            
            int_results = {}
            if self.data.prior_test_data is not None:
                int_results['samples'] = self.data.prior_test_indicies
                int_results['results'] = self.data.blind_prediction_results[n]
            else:
                int_results['samples'] = None
                int_results['results'] = None
            
            preds = np.asarray(self.data.prediction_results[n])

            int_results["Silhouette"] = metrics.silhouette_score(self.data.test_data,preds)
            int_results['CH Score'] = metrics.calinski_harabasz_score(self.data.test_data,preds)
            
            if self.data.feature_importances[n] == None:
                int_results["Features"] = self.fi_interpret()

            
            all_results[tech] = int_results
            
        '''ALLRESULTS - a dict of dicts which will be returned to frontend '''
        all_results['best'] = self.assign_top_model_unsup(all_results)
        all_results['education'] = self.data.educational_info
        all_results['analysis type'] = 'unsupervised'
        
        self.data.interpreted_results = all_results

        return self.data
    
    
    
    def fi_interpret(self,feat_imp):
        
        feature_ranking,_ = two_list_sort(self.data.original_features,feat_imp)
        feature_ranking.reverse()
        return feature_ranking
        

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
          self.data.data_for_update.append((technique,class_results[technique]["F1 Score"],self.data.descriptive_info))

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

        
          self.data.data_for_update.append((technique,class_results[technique]["Silhouette"],self.data.descriptive_info))
        return best_technique


def two_list_sort(tosort,basis):
    
    for i in range(1, len(basis)):
        key = basis[i]
        key2 = tosort[i]
        j = i-1
        while j >=0 and key <basis[j] :
            basis[j+1] = basis[j]
            tosort[j+1] = tosort[j]
            j -= 1
        
        basis[j+1] = key
        tosort[j+1] = key2
            
    return tosort,basis
