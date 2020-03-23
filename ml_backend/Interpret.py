#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: 

Standardization class for Results collection/model eval

"""

from sklearn import metrics
import copy 

class INTERPRET:
    
    def __init(self,data):
        self.data = copy.deepcopy(data)
        
        
    def interpret_supervised():
        pass
    
    def interpret_unsupervised():
        pass
    
    def supervised_accuracy_metrics(self):
        
        techniques = self.data.get_techniques()
        true_labels = self.data.get_labels()
        
        all_results = {}
        
        for n,tech in enumerate(techniques):
            
            int_results = {}
            preds = self.data.get_prediction_results[n]
            fpr, tpr, _ = metrics.roc_curve(true_labels,preds)
            
            int_results["Accuracy"] = metrics.accuracy_score(true_labels,preds)
            int_results["AUC"] = metrics.auc(fpr, tpr)
            int_results['F1 Score'] = metrics.f1_score(true_labels,preds)
            
            cm = metrics.confusion_matrix(true_labels, preds)
            
            int_results = self.analyze_confusion_metrics(cm,true_labels,int_results)
        
            all_results[tech] = int_results
        
        self.data.add_interpreted_results(all_results)
        
        return self.data
            
 
    def uns_accuracy_metrics(self):
        pass
    
    def fi_interpret(self):
        pass 
    
    def analyze_confusion_metrics(self):
        pass
        
    def NL_results(self,name):
        pass
    
    def assign_top_model(self):
        pass
    
    def update_model_heuristics(self):
        pass
  

    
        
        
    
    
    
    