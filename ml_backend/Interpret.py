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
        all_results = {"techniques":{"names":[],"samples":[],"results":[],"accuracy":[],
                                     "f1_score":[],"silhouette":[],"ch_score":[],"feature_importances":[]}}
        
        ## TODO: run for all techniques - currently just 1
        for n,tech in enumerate(techniques):
            all_results['techniques']['names'].append(tech)
            if self.data.prior_test_data is not None:
                all_results['techniques']['samples'].append(self.data.prior_test_indicies)
                all_results['techniques']['results'].append(self.data.blind_prediction_results[n])
            else:
                 all_results['techniques']['samples'].append([]) 
                 all_results['techniques']['results'].append([]) 
 
            preds = np.asarray(self.data.prediction_results[n])
            true_labels = np.asarray(self.data.test_labels[n])

            if self.data.feature_importances[n] is not None:
                 all_results['techniques']["feature_importances"].append(self.fi_interpret(self.data.feature_importances[n]))
            else:
                 all_results['techniques']["feature_importances"].append([])
            
            all_results['techniques']["accuracy"].append(metrics.accuracy_score(true_labels,preds))
            all_results['techniques']['f1_Score'].append(metrics.f1_score(true_labels,preds,average='macro'))
            all_results['techniques']['silhouette'] = None
            all_results['techniques']['ch_score'] = None
            all_results['techniques']["confusion_matrix"] = metrics.confusion_matrix(true_labels, preds)
            # int_results["NL Results"] = self.NLResults()

        all_results['best'] = self.assign_top_model_sup(all_results)
        all_results['analysis type'] = 'supervised'
        all_results['labels'] = list(set(self.data.labels))
        all_results['education'] = self.data.educational_info
        
        self.data.interpreted_results = all_results
        return self.data
            
 
    def uns_accuracy_metrics(self):
           
        techniques = self.data.techniques


        all_results = {"techniques":{"names":[],"samples":[],"results":[],"accuracy":[],
                                     "f1_score":[],"silhouette":[],"cH_score":[],"feature_importances":[]}}
        
        ## TODO: run for all techniques - currently just 1
        ### TODO: add more eval methods??
        
        for n,tech in enumerate([techniques[-1]]):

            all_results['techniques']['names'].append(tech)
            
            if self.data.prior_test_data is not None:
                all_results['techniques']['samples'].append(self.data.prior_test_indicies)
                all_results['techniques']['results'].append(self.data.blind_prediction_results[n])
            else:
                 all_results['techniques']['samples'].append([]) 
                 all_results['techniques']['results'].append([]) 
            preds = np.asarray(self.data.prediction_results[n])

            all_results['techniques']["Silhouette"] = metrics.silhouette_score(self.data.test_data,preds)
            all_results['techniques']['ch_Score'] = metrics.calinski_harabasz_score(self.data.test_data,preds)
            all_results['techniques']['accuracy'] = None
            all_results['techniques']['f1_Score'] = None
            all_results['techniques']["confusion_matrix"] = None
            
            if self.data.feature_importances[n] == None:
                all_results['techniques']["feature_importances"] = self.fi_interpret()
            else:
                all_results['techniques']["feature_importances"].append([])
            

           
        '''ALLRESULTS - a dict of dicts which will be returned to frontend '''
        all_results['best'] = self.assign_top_model_unsup(all_results)
        all_results['education'] = self.data.educational_info
        all_results['analysis type'] = 'unsupervised'
        all_results['labels'] = list(set(self.data.labels))
        
        
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
