#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: 

Standardization class for Results collection/model eval

"""

from sklearn import metrics
import copy 
import numpy as np
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt


class INTERPRET:
    
    
    def __init__(self,data,performance_threshold):
        
        self.data = copy.deepcopy(data)
        self.performance_threshold = performance_threshold

        
    def interpret_supervised(self):
        
        self.data = self.supervised_accuracy_metrics()
        
       # if self.data.feature_importances is not None:
        #    self.data = self.fi_interpret()
        
       # self.data = self.assign_top_model()
       # self.data = self.NLResults()
       # self.data = self.assign_top_model()
        
        return self.data
    
    def interpret_unsupervised():
        pass
    
    def supervised_accuracy_metrics(self):
        
        techniques = self.data.techniques

        all_results = {}
        
        for n,tech in enumerate([techniques[-1]]):
            
            int_results = {}
            
            preds = np.asarray(self.data.prediction_results[n][0])
            true_labels = np.asarray(self.data.test_labels)

            # Compute ROC curve and ROC area for each class + cite sklearn
            
            fpr = {}
            tpr = {}
            roc_auc = []
            
            for i in range(len(list(set(true_labels)))):
                fpr[i], tpr[i], _ = metrics.roc_curve(true_labels, preds,pos_label=list(set(true_labels))[i])
                roc_auc.append(metrics.auc(fpr[i], tpr[i]))

            int_results["Accuracy"] = metrics.accuracy_score(true_labels,preds)
            int_results["AUC"] = np.median(roc_auc)
            int_results['F1 Score'] = metrics.f1_score(true_labels,preds,average='macro')

            int_results["Confusion Matrix"] = metrics.confusion_matrix(true_labels, preds)
            

            all_results[tech] = int_results
        
        self.data.interpreted_results = all_results

        return self.data
            
 
    def uns_accuracy_metrics(self):
        pass
    
    def fi_interpret(self):
        pass 
    


    def NL_results(self,name):
        pass
    
    
    def assign_top_model(self,class_results):
        
        best_technique = None
        highest_AUC = 0
        
        for technique in class_results.keys():
            
          self.update_result_tup(technique,class_results[technique]["AUC"])
          
          if class_results[technique]["AUC"] > highest_AUC:
                highest_AUC = class_results[technique]["AUC"]
                best_technique = technique
                
          if class_results[technique]["AUC"] == highest_AUC:
              if class_results[technique]["F1 Score"] < class_results[best_technique]["F1 Score"]:
                    best_technique = technique
                    
              if class_results[technique]["Accuracy"] == class_results[best_technique]["Accuracy"]:
                   if class_results[technique]["Accuracy"] < class_results[best_technique]["Accuracy"]:
                        best_technique = technique
                        
                   if class_results[technique]["Accuracy"] == class_results[best_technique]["Accuracy"]:
                        if np.random.randint(0,2) > 0:
                            best_technique = technique

        self.data.set_best_model((best_technique,class_results[best_technique]["AUC"]))
        return self.data
        
    
    
    
    def update_result_tup(self,technique,score):
        
         for n,tup in enumerate(self.data.data_for_update):
             
             if technique in tup:
                ml_update = list(self.data.data_for_update[n])
                ml_update.append(score)
                self.data.data_for_update[n] = tuple(ml_update)
                
         #### TBC 
         pass
     