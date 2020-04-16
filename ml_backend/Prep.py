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
import string

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
                
        self.data_for_update = []
        
        ### for images only 
        self.dimensions = None
        
        self.evalscore = 1
        
        self.analysis_type = None
        
        self.original_features = None
        
        self.test_data = []
        
        self.test_labels = []

        self.prior_test_data = None

        self.prior_test_indicies = None

        self.blind_prediction_results = []

        self.educational_info = []

        
        

class DATAPREP:
    
    def __init__(self,datafiles,datafilenames,datafilesize,labelfile,labelfilename,labelfilesize,info_dict):
    
        self.data = DATA()
        self.datafiles = datafiles
        self.info_dict = info_dict
        self.labelfile = labelfile
        self.datafilenames = datafilenames
        self.labelfilename = labelfilename
        self.datafilesize = datafilesize
        self.labelfilesize = labelfilesize
        
        
    def run(self):
       
        self.data = self.from_fileobject()
        return self.eval_data()

    def from_fileobject(self):
        
        data_files = []

        for n,file in enumerate(self.datafiles):
            data_files.append(self.process_data(file,self.datafilenames[n],self.datafilesize[n]))

        
        if len(data_files) > 1:
            data_files = self.consolidate_data(data_files)
        else:
            self.data.data = data_files[0][0]
        
    
        if self.labelfile is not None:
             self.data.labels = self.process_labels()
             self.data.analysis_type = 'supervised'
             
        elif self.data.data_type == 'numeric' and self.labelfile is None:
            self.extract_labels()
            print("here")
        else:
            self.data.labels = None
            self.data.analysis_type = 'unsupervised'
        
        self.data.time_constraint = int(self.info_dict["time"])
        self.data.descriptive_info = self.process_user_info(str(self.info_dict["user_input"]))
        self.data.userid = str(self.info_dict["userid"])
        
        return self.data
    
    
    
    def process_data(self,file,filename,filesize):
        
        
        if str(filename).find('.jpg') > -1 or str(filename).find('.png') > -1:
            self.data.data_type = "image"
            file.stream.seek(0)
            file.save(str(self.info_dict['userid']) + filename,filesize)
            output = np.asarray(cv2.imread(str(self.info_dict['userid']) + filename,cv2.IMREAD_GRAYSCALE))
            self.data.dimension = output.shape
            os.remove(str(self.info_dict['userid']) + filename)
            return (output,filename)


        if str(filename).find('.xlsx') > -1:
            self.data.data_type = "numeric"
            file.stream.seek(0)
            file.save(str(self.info_dict['userid']) + filename,filesize)
            output = pd.read_excel(str(self.info_dict['userid']) + filename)
            os.remove(str(self.info_dict['userid']) + filename)
            return (output,filename)

            
        if str(filename).find('.csv') > -1:
            self.data.data_type = "numeric"
            file.stream.seek(0)
            file.save(str(self.info_dict['userid']) + filename,filesize)
            output=pd.read_csv(str(self.info_dict['userid']) + filename)
            os.remove(str(self.info_dict['userid']) + filename)
            return (output,filename)
  
  
    
    def process_user_info(self,userinput):
        
        words =  nltk.word_tokenize(userinput) 
        words = [word.lower() for word in words if word not in string.punctuation or word == '.']
        tagged_words = nltk.pos_tag(words)
        search_words = []
        bigram = False
        for n,word in enumerate(tagged_words):
 
            if n < len(tagged_words)-1:
                if (word[1][0] == 'N' and tagged_words[n+1][1][0] == 'J') or (word[1][0] == 'N' and tagged_words[n+1][1][0] == 'N'):
                    if word[0] + " " + tagged_words[n+1][0] not in search_words:
                        search_words.append(word[0] + " " + tagged_words[n+1][0])
                    bigram = True

            if (word[1][0] == 'N') and word[0].find('data') == -1 and not bigram:
                    if word[0] not in search_words:
                        search_words.append(word[0])
        
            bigram = False
        
        return search_words
  
        

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
            

    
    def consolidate_data(self,datafiles):
        
        data = pd.DataFrame()
        testdata = pd.DataFrame()
        
        for n,entry in enumerate(datafiles):
          if entry[1].find('test') == -1:
              if self.data.data_type == 'image':
                  data.loc[entry[1]] = np.reshape(entry,data.dimensions[0]*data.dimensions[1])
              if self.data.data_type == 'numeric':
                   if n == 0:
                       data = entry[0]
                   else:
                       data = pd.concat([data,entry[0]],0)
          else:
             if self.data.data_type == 'image':
                  testdata.loc[entry[1]] = np.reshape(entry,data.dimensions)
             if self.data.data_type == 'numeric':
                if n == 0:
                    testdata = entry[0]
                else:
                    testdata = pd.concat([data,entry[0]],0)

        self.data.data = data
        self.data.prior_test_data = testdata.values
        self.data.prior_test_indicies = list(testdata.index)
        self.data.original_features = list(data.columns)
        
        
    
    def extract_labels(self):

        self.data.original_features = list(self.data.data.columns)

        for n,col in enumerate(self.data.data.columns):
            if str(col).lower().find('label') > -1:
                self.data.labels = self.data.data[col].values
                print(self.data.labels)
                self.data.data.drop(col,1)
                self.data.analysis_type = 'supervised'
                self.data.data = self.data.data.values
                return
        
        self.data.data = self.data.data.values
        self.data.analysis_type = 'unsupervised'
    
    
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
                 
            
        if sparsity > 0.25:
            score -= 0.15
             
        if oratio > 0.1:
                score -= 0.1

        if self.get_label_ratios() > (1/len(set(self.data.labels)))/2:
                    score -= 0.1
        
        
        self.data.descriptive_info.extend(data_features)
        info = self.data.descriptive_info
        self.data.descriptive_info = []
        print()
        self.data.descriptive_info = separate_bigrams(list(itertools.combinations(info,2)))
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

def separate_bigrams(lst):
    
    lst2 = []
    for tup in lst:
        if len(tup[0].split()) > 1:
            if (tup[0],"") not in lst2:
                lst2.append((tup[0],""))
            if len(tup[1].split()) > 1:
                if (tup[1],"") not in lst2:
                    lst2.append((tup[1],""))
                continue
            continue
        lst2.append(tup)
            
    return lst2
            
        
            
            
        



    
