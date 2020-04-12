#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:44:58 2020

@author: anibaljt
"""

import numpy as np
import nltk
import cv2
import pandas as pd
import itertools
import os 

class DATA:
    
    def __init__(self):
        
        
        ''' the data that is to be analyzed ''' 
        self.data = None
        
        ''' the class labels for the data that is to be analyzed ''' 
        self.labels = None
        
        self.userid = None
        
        self.data_type = None
        
        self.descriptive_info = []
        
        self.bestmodel = None
        
        self.techniques = []

        self.time_constraint = None
        
        self.feature_importances = []
        
        self.interpreted_results = None
        
        self.prediction_results = []
                
        self.data_for_update = None
        
        ### for images only 
        self.dimensions = None
        
        self.evalscore = 1
        
        self.analysis_type = None
        
        self.original_features = None
        
        self.test_data = []
        
        self.test_labels = []
        
        


class DATAPREP:
    
    def __init__(self,datafiles,datafilenames,datafilesize,labelfile,labelfilename,labelfilesize,info_dict):
    
        self.data = DATA()
        self.data.userid = info_dict["userid"]
        self.datafiles = datafiles
        self.info_dict = info_dict
        self.labelfile = labelfile
        self.datafilenames = datafilenames
        self.labelfilename = labelfilename
        self.datafilesize = datafilesize
        self.labelfilesize = labelfilesize
        
        
    def run(self):
        pass

    def from_fileobject(self):
        
        data_files = []
        
        for n,file in self.datafiles:
            data_files.append(self.process_data(file,self.datafilenames[n],self.datafilesize[n]))


        if len(data_files) > 1:
            data_files = self.consolidate_data(data_files)
        self.data.data = data_files
    
    
        if self.labelfile is not None:
             self.data.labels = self.process_labels()
             self.data.analysis_type = 'supervised'
             
        elif self.data.type == 'numeric' and self.labelfile is None:
            self.data.labels = self.extract_labels()
            
        else:
            self.data.labels = None
            self.data.analysis_type = 'unsupervised'
        
        
        self.data.time_constraint = int(self.user_dict["time"])
        self.data.descriptive_information = str(self.user_dict["user_input"])
        self.data.user_id = str(self.user_dict["userid"])
        
        return self.data
    
    
    
    def process_data(self,file,filename,filesize):
        
        
        if str(filename).find('.jpg') > -1 or str(filename).find('.jpg') > -1:
            self.data.data_type = "image"
            file.save(str(self.info_dict['userid']) + filename,filesize)
            output = np.asarray(cv2.imread(file,cv2.IMREAD_GRAYSCALE))
            self.data.dimension = output.shape
            os.remove(str(self.info_dict['userid']) + filename)
            return (output,filename)


        if str(filename).find('.txt') > -1 or str(filename).find('.text') > -1:
            self.data.data_type = "text"
            file.save(str(self.info_dict['userid']) + filename,filesize)
            string = ""
            with open(str(self.info_dict['userid']) + filename, 'r') as f:
                for line in f.readlines():
                    string += str(line)
            f.close()
            os.remove(str(self.info_dict['userid']) + filename)
            return (self.process_txt(filename),filename)
        
        
        if str(filename).find('.xlsx') > -1:
            self.data.data_type = "numeric"
            file.save(str(self.info_dict['userid']) + filename,filesize)
            output = pd.read_excel(filename)
            os.remove(str(self.info_dict['userid']) + filename)
            return (output,filename)

            
        if str(filename).find('.csv') > -1:
            self.data.data_type = "numeric"
            file.save(str(self.info_dict['userid']) + filename,filesize)
            output = pd.read_csv(filename)
            os.remove(str(self.info_dict['userid']) + filename)
            return (output,filename)
  
  

    def process_labels(self):
        
        
        self.labelfile.save(str(self.info_dict['userid']) + self.labelfilename,self.labelfilesize)
        
        if str(self.labelfilename).find('.csv') > -1:
            output = pd.read_csv(self.labelfilename)
        else:
            output = pd.read_excel(self.labelfilename)
            
        os.remove(str(self.info_dict['userid']) + self.labelfilename)
        names = output.columns[0] 
        
        labels = []
        for name in self.datafilenames:
            labels.append(names.index(name))
        
        return np.asarray(labels)
            

    
    def consolidate_data(self):
        
        data = pd.DataFrame()
        for n,entry in enumerate(self.data.data):
            if self.data.data_type == 'image':
                data.loc[n] = np.reshape(entry,data.dimensions)
            if self.data.data_type == 'numeric':
                if n == 0:
                    data = entry
                else:
                    data = pd.concat([data,entry],0)

        self.data.data = data.values
        self.data.original_features = list(data.columns)
        
        
    
    def extract_labels(self):
        
        for n,col in enumerate(self.data.original_features):
            if str(col).lower() == 'labels':
                self.data.labels = self.data.data[n]
                self.data.data = np.delete(self.data,n)
                self.data.analysis_type = 'supervised'
                return
            
        self.data.analysis_type = 'unsupervised'
                

    ### TODO: add in text data handling
    def eval_text_data(self):
        pass
    
    
    def eval_data(self):
        
        score = 1
        data_features = []

        if self.data.descriptive_info == None:  ###or in list form??
            score -= 0.25


        nan_count = 0
        for arr in self.data.data:
            nan_count += list(np.isnan(arr)).count('True')
            
        sparsity = nan_count/len(self.data.data)
        oratio = self.outlier_ratio(self.data.data)/len(self.data.data)
                 
        if sparsity > 0.1:
            data_features.append("sparse")
            if sparsity > 0.25:
                score -= 0.15
             
        if oratio > 0.05:
             data_features.append("outliers")
             if oratio > 0.1:
                score -= 0.1
                       
        if len(self.data.labels) < 100:
            data_features.append("small dataset")
            if len(self.data.labels) < 25:
                score -= 0.25
        
        if self.data.analyis_type == 'supervised':
            if len(list(set(self.data.labels))) > 2:
                data_features.append("multiclass")
            
            elif len(list(set(self.data.labels))) == 2:
                data_features.append("binary")
            
            else:
                data_features.append("one-class")
        
         
            if self.get_label_ratios() > (1/len(set(self.data.labels)))/3:
                data_features.append("imbalance")
                if self.get_label_ratios() > (1/len(set(self.data.labels)))/2:
                    score -= 0.1
        

        self.data.descriptive_info.extend(data_features)
        info = self.data.descriptive_info
        self.data.descriptive_info = []
        self.data.descriptive_info = list(itertools.combinations(info,2))
        self.data.eval_score = score
        
        return self.data
    
 
    
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


    def outlier_ratio(self,data):
        
        data = pd.DataFrame(data)
        outlier_ratio = 0
        
        for i in data.columns:
            mean = np.mean(data[i].values)
            std = np.std(data[i].values)
            
            if std > 0:
                vals = (data[i].values-mean)/std
            else:
                vals = data[i].values-mean
                
            outliers = np.where(np.abs(vals) > 3)[0]
            if len(outliers) > 0:
                outlier_ratio  += (len(outliers)/len(data[i]))
        
        return outlier_ratio