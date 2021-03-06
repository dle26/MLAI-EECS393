#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: 

Standardization class for Results collection/model eval

"""

from sklearn import metrics
import copy 
from ml_backend.UpdateAgent import UpdateAgent as UA
import numpy as np


class INTERPRET:
    
    
    def __init__(self,data,performance_threshold=0.6):
        
        self.data = copy.deepcopy(data)
        self.performance_threshold = performance_threshold
     
        
    def interpret(self):
        
        if self.data.analysis_type == 'supervised':
           interp =  self.supervised_accuracy_metrics()
          # if len(self.data.descriptive_info) > 0:
               #UA.update(self.data.data_for_update,self.data.evalscore)
           return interp
           
        interp = self.uns_accuracy_metrics()
        #if len(self.data.descriptive_info) > 0:
          # UA.update(self.data.data_for_update,self.data.evalscore)

        return interp
        

    
    def supervised_accuracy_metrics(self):
        
        techniques = self.data.techniques
        all_results = {"techniques":{"names":[],"samples":[],"results":[],"accuracy":[],
                                     "f1_score":[],"silhouette":[],"ch_score":[],"feature_importances":[],'confusion_matrix':[]}}
        
        ## TODO: run for all techniques - currently just 1
        for n,tech in enumerate(techniques):
            print(tech)
            all_results['techniques']['names'].append(tech)
            if self.data.prior_test_data is not None:
                
                str_results = []
                for pti in self.data.prior_test_indicies:
                    str_results.append(str(pti))
                all_results['techniques']['samples'].append(str_results)
                
                str_results = []
                for bpr in self.data.blind_prediction_results[n]:
                    str_results.append(str(bpr))
                all_results['techniques']['results'].append(str_results)
        
            else:
                 all_results['techniques']['samples'].append([]) 
                 all_results['techniques']['results'].append([]) 
 
            preds = np.asarray(self.data.prediction_results[n])
            true_labels = np.asarray(self.data.test_labels[n])

            if self.data.feature_importances[n] is not None:
                 all_results['techniques']["feature_importances"].append(self.fi_interpret(self.data.feature_importances[n]))
            else:
                 all_results['techniques']["feature_importances"].append([])
            
            all_results['techniques']["accuracy"].append(float(metrics.accuracy_score(true_labels,preds)))
            all_results['techniques']['f1_score'].append(float(metrics.f1_score(true_labels,preds,average='macro')))
            all_results['techniques']['silhouette'] = None
            all_results['techniques']['ch_score'] = None
            
            cm_list = []
            cm = metrics.confusion_matrix(true_labels, preds,normalize='true')
            for element in cm:
                newelement = []
                for number in element:
                    newelement.append(float(number))
                cm_list.append(newelement)
            
            all_results['techniques']["confusion_matrix"].append(cm_list)

        all_results['best'] = self.assign_top_model_sup(all_results)
        all_results['analysis type'] = 'supervised'
        lbls = []
        for i in self.data.label_names:
            lbls.append(str(i))
        
        all_results['labels'] = lbls
        all_results['education'] = self.data.educational_info
        
        self.data.interpreted_results = all_results
        return self.data
            
 
    def uns_accuracy_metrics(self):
           
        techniques = self.data.techniques


        all_results = {"techniques":{"names":[],"samples":[],"results":[],"accuracy":[],
                                     "f1_score":[],"silhouette":[],"ch_score":[],"feature_importances":[]}}
        
        ## TODO: run for all techniques - currently just 1
        ### TODO: add more eval methods??
        
        for n,tech in enumerate(techniques):

            all_results['techniques']['names'].append(tech)
            
            if self.data.prior_test_data is not None:
                
                str_results = []
                for pti in self.data.prior_test_indicies:
                    str_results.append(str(pti))
                all_results['techniques']['samples'].append(list(self.data.prior_test_indicies))
               
                str_results = []
                for bpr in self.blind_prediction_results[n]:
                    str_results.append(str(bpr))
                all_results['techniques']['results'].append(str_results)
        
            else:
                 all_results['techniques']['samples'].append([]) 
                 all_results['techniques']['results'].append([]) 
            preds = np.asarray(self.data.prediction_results[n])

            all_results['techniques']["silhouette"].append(float(metrics.silhouette_score(self.data.test_data[n],preds)))
            all_results['techniques']['ch_score'].append(float(metrics.calinski_harabasz_score(self.data.test_data[n],preds)))
            all_results['techniques']['accuracy'] = None #.append(float(metrics.silhouette_score(self.data.test_data[n],preds)))
            all_results['techniques']['f1_score'] = None #.append(float(metrics.calinski_harabasz_score(self.data.test_data[n],preds)))
            all_results['techniques']["confusion_matrix"] = [[],[]]
            
            if self.data.feature_importances[n] is not None:
                all_results['techniques']["feature_importances"].append(self.fi_interpret())
            else:
                all_results['techniques']["feature_importances"].append([])
            

           
        '''ALLRESULTS - a dict of dicts which will be returned to frontend '''
        all_results['best'] = self.assign_top_model_unsup(all_results)
        all_results['education'] = self.data.educational_info
        all_results['analysis type'] = 'unsupervised'
        all_results['labels'] = []
        
        
        self.data.interpreted_results = all_results

        return self.data
    
     
    
    def fi_interpret(self,feat_imp):
        
        feature_ranking,feats = two_list_sort(self.data.original_features,feat_imp)
        feature_ranking.reverse()
        feature_ranking = np.asarray(feature_ranking)[[f for f in range(len(feats)) if feats[f] > 0]]
        return list(feature_ranking)[0:3]
        

    def assign_top_model_sup(self,class_results):
        
        best_technique = None
        highest_F1 = 0
        for n,f1 in enumerate(class_results['techniques']['f1_score']):
            
          if f1 > highest_F1:
                highest_F1 = f1
                best_technique = class_results['techniques']["names"][n]
                bt_index = n
          
          if f1 == highest_F1:
              if class_results['techniques']["accuracy"][n] > class_results['techniques']["accuracy"][bt_index]:
                    best_technique = class_results['techniques']["names"][n]
                    bt_index = n
                        
              elif class_results['techniques']["accuracy"][n] == class_results['techniques']["accuracy"][bt_index]:
                  if np.random.randint(0,2) > 0:
                       best_technique = class_results['techniques']["names"][n]
                       bt_index = n
                           
          self.data.data_for_update.append((class_results['techniques']["names"][n],highest_F1,self.data.descriptive_info))

        return best_technique
    

    def assign_top_model_unsup(self,class_results):
        
        best_technique = None
        highest_sil = 0
        
        for n,ss in enumerate(class_results['techniques']['silhouette']):
            
          
          if ss > highest_sil:
                highest_sil = ss
                best_technique = class_results['techniques']["names"][n]
                bt_index = n
                
          if ss == highest_sil:
              if class_results['techniques']["ch_score"][n] > class_results['techniques']["ch_score"][bt_index]:
                    best_technique = class_results['techniques']["names"][n]
                    bt_index = n
                        
              elif class_results['techniques']["ch_score"][n] == class_results['techniques']["ch_score"][bt_index]:
                  if np.random.randint(0,2) > 0:
                       best_technique = class_results['techniques']["names"][n]
                       bt_index = n

        
          self.data.data_for_update.append((class_results['techniques']["names"][n],highest_sil,self.data.descriptive_info))
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
