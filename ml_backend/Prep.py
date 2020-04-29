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
import spacy


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
        
        self.label_names = {}
        
        self.search_queries = None

        
        

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
        
        if self.data.labels is not None:
            self.data.labels,self.data.label_names = map_labels(self.data.labels)
        
        if len(list(set(self.data.label_names))) < 2:
            self.data.analysis_type = 'unsupervised'
        
        self.data.original_features = list(self.data.data.columns)
        self.data.data = self.data.data.values
        
        self.data.time_constraint = int(self.info_dict["time"])
        self.data.search_queries = self.process_user_info(str(self.info_dict["user_input"]),False)
        self.data.descriptive_info = self.process_user_info(str(self.info_dict["user_input"]),True)
        self.data.userid = str(self.info_dict["userid"])
        
        return self.data
    
    
    
    def process_data(self,file,filename,filesize):

        if str(filename).find('.jpg') > -1 or str(filename).find('.png') > -1:
            self.data.data_type = "image"
            file.stream.seek(0)
            file.save(str(self.info_dict['userid']) + filename,filesize)
            output = np.asarray(cv2.imread(str(self.info_dict['userid']) + filename,cv2.IMREAD_GRAYSCALE))
            self.data.dimensions = output.shape
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
  
  
    
    def process_user_info(self,userinput,synonyms=False):
        
        nlp = spacy.load('en_core_web_lg')
        doc = nlp(userinput.lower())
        tagged_words = []
        for token in doc:
            tagged_words.append((token.text,token.pos_))
        
        search_words = []
        bigram = False
        bigram_tags = ["PROPN","NOUN","ADJ"]
        word_tags = bigram_tags[0:-1]

        for n,word in enumerate(tagged_words):
 
            if n < len(tagged_words)-1:
                if (word[1] in bigram_tags and tagged_words[n+1][1] in bigram_tags):
                  if (word[0].find('data') == -1 and tagged_words[n+1][0].find('data') == -1):
                    if str(search_words).find(word[0]) == -1 and str(search_words).find(tagged_words[n+1][0]) == -1:
                        search_words.append(word[0] + " " + tagged_words[n+1][0])
                        if synonyms:
                            search_words = create_bigram_synonyms(word[0] + " " + tagged_words[n+1][0], search_words,nlp,bigram_tags)
                    bigram = True

            if (word[1] in word_tags and not bigram and word[0].find('data') == -1):
                if str(search_words).find(word[0]) == -1:
                        search_words.append(word[0])
                        if synonyms:
                            search_words = create_word_synonyms(word[0], search_words,nlp,word_tags)
        
            bigram = False
            
        return search_words
  
        

    def process_labels(self):
        
        self.labelfile.stream.seek(0)
        self.labelfile.save(str(self.info_dict['userid']) + self.labelfilename,self.labelfilesize)

        
        if str(self.labelfilename).find('.csv') > -1:
            output = pd.read_csv(str(self.info_dict['userid']) + self.labelfilename)
        else:
            output = pd.read_excel(str(self.info_dict['userid']) + self.labelfilename)
            
        os.remove(str(self.info_dict['userid']) + self.labelfilename)
        names = output.columns 
        
        labels = []
        for name in names:
            if name.lower().find('label') > -1:
                for lb in output[name]:
                    labels.append(lb)
    
        return np.asarray(labels)
            

    
    def consolidate_data(self,datafiles):
        
        newdata = pd.DataFrame()
        testdata = None
        
        for n,entry in enumerate(datafiles):
          if entry[1].find('test') == -1:
              if self.data.data_type == 'image':
                  if n == 0:
                    newdata = pd.DataFrame(np.reshape(entry[0],self.data.dimensions[0]*self.data.dimensions[1])).T
                    newdata.index=[entry[1]]
                  else:
                      newdata.loc[entry[1]] = np.reshape(entry[0],self.data.dimensions[0]*self.data.dimensions[1])
              if self.data.data_type == 'numeric':
                   if n == 0:
                       newdata = entry[0]
                   else:
                       newdata = pd.concat([newdata,entry[0]],0)
          else:
             if self.data.data_type == 'image':
                 if n == 0:
                     testdata = pd.DataFrame(np.reshape(entry[0],self.data.dimensions[0]*self.data.dimensions[1])).T
                     testdata.index = index=[entry[1]]
                 else:
                    testdata.loc[entry[1]] = np.reshape(entry[0],self.data.dimensions[0]*self.data.dimensions[1])
                  
             if self.data.data_type == 'numeric':
                if n == 0:
                    testdata = entry[0]
                else:
                    testdata = pd.concat([testdata,entry[0]],0)

        self.data.data = newdata
        if testdata is not None:
            self.data.prior_test_data = testdata.values
            self.data.prior_test_indicies = list(testdata.index)

        

    def extract_labels(self):
        
        for n,col in enumerate(self.data.data.columns):
            if str(col).lower().find('label') > -1:
                self.data.labels = self.data.data[col].values
                self.data.data = self.data.data.drop([col],1)
                self.data.analysis_type = 'supervised'
                return
    
    
        self.data.analysis_type = 'unsupervised'
    
    
    def eval_data(self):
        score = 1

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
        print(self.data.labels)
        
        if self.data.labels is not None:
            if self.get_label_ratios() > (1/len(set(self.data.labels)))/2:
                    score -= 0.1
        
        
        if len(self.data.descriptive_info) > 1:
            self.data.descriptive_info = separate_bigrams(list(itertools.combinations(self.data.descriptive_info,2)))
        if len(self.data.search_queries) == 1:
            self.data.search_queries = [(self.data.search_queries[0],)]
        else:
            self.data.search_queries = separate_bigrams(list(itertools.combinations(self.data.search_queries,2)))
            
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




''' --------------- UTILS ----------------- '''

def separate_bigrams(lst):
    
    lst2 = []
    for tup in lst:
        first = False
        second = False
        if len(tup[0].split()) > 1:
            if (tup[0],"") not in lst2:
                lst2.append((tup[0],""))
            first = True
        if len(tup[1].split()) > 1:
            if (tup[1],"") not in lst2:
                lst2.append((tup[1],""))
            second = True
    
        if first and not second:
            lst2.append(tup)
            lst2.append((tup[1],""))
            continue
        if not first and second:
            lst2.append(tup)
            lst2.append((tup[0],""))
            continue
        if not first and not second:
            lst2.append(tup)
            
    return lst2
      

      
def map_labels(labels):
    
    label_set = list(set(labels))
    label_dict = {}
    
    for n,label in enumerate(label_set):
        label_dict[int(n)] = label
        
    
    new_labels = []
    for label in labels:
        new_labels.append(label_set.index(label))
    
    return new_labels,list(label_dict.values())


def most_similar(word):
    
    synonyms = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    synonyms = sorted(synonyms, key=lambda w: word.similarity(w), reverse=True)
    return [w.lower_ for w in synonyms[:3]]


def create_bigram_synonyms(bigram,current_words,model,tags):
    
    for n,word in enumerate(bigram.split()):
        synonyms = most_similar(model.vocab[word])
        for syn in synonyms:
            for tok in model(syn):
                if tok.pos_ in tags and str(current_words).find(syn) == -1:
                    if n == 0:
                        current_words.append(syn + " " + bigram.split()[1])
                    else:
                        current_words.append(bigram.split()[0] + " " + syn)
    return current_words



def create_word_synonyms(word,current_words,model,tags):

    synonyms = most_similar(model.vocab[word])

    for syn in synonyms:
        for tok in model(syn):
            if tok.pos_ in tags and str(current_words).find(syn) == -1:
                current_words.append(syn)

    return current_words
