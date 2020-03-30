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
    
    #### TODO: Score the quality data based on heuristics 
    
    def __init(self,data,performance_threshold,data_score):
        self.data = copy.deepcopy(data)
        self.data_score = data_score

        
    def interpret_supervised(self):
        
        self.data = self.supervised_accuracy_metrics()
        
        if self.data.get_feat_importances() is not None:
            self.data = self.fi_interpret()
        
        self.data = self.assign_top_model()
        self.data = self.NLResults()
        self.data = self.assign_top_model()
        
        return self.data
    
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
            
            int_results["Class Predictions"] = self.analyze_confusion_metrics(cm,true_labels,int_results)
        
            all_results[tech] = int_results
        
        self.data.add_interpreted_results(all_results)
        
        return self.data
            
 
    def uns_accuracy_metrics(self):
        pass
    
    def fi_interpret(self):
        pass 
    
    def analyze_confusion_metrics(self,cm):
        

       preds_by_labels = {}
       j = 0
       
       for num,i in enumerate(list(cm)):
          preds_by_labels[str(num)+"correct"] = i
          if (j/2)%0:
              preds_by_labels[str(num)+"false prediction"] = i/len(cm)
              j = 0
              
       return preds_by_labels
             

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
                ml_update,ppr_update = list(self.data.data_for_update[n]),list(self.data.ppr_data_for_update[n])
                ml_update.append(score)
                ppr_update.append(score)
                self.data.data_for_update[n],self.data.ppr_data_for_update[n] = tuple(ml_update),tuple(ppr_update)   