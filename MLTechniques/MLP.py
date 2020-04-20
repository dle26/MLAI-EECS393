#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 00:11:58 2020

@author: anibaljt
"""


from .Technique import Technique
import torch
import torch.nn as nn
import torch.optim as optim
import random
import torch.nn.functional as F
import numpy as np
from sklearn.preprocessing import StandardScaler


class MLP(Technique):
    
    class Perceptron(nn.Module):
        
        def __init__(self,input_size,hidden_size,n_classes,extratime = False):
            
            super(MLP.Perceptron, self).__init__()
            self.input_size = input_size
            self.hidden_size  = hidden_size
            self.n_classes = n_classes
                        
            if not extratime:
                self.layer1 = nn.Sequential(nn.Dropout(0.2),
                                            nn.Linear(self.input_size, self.hidden_size),
                                            nn.LeakyReLU(),
                                            nn.Linear(self.hidden_size,self.hidden_size),
                                            nn.LeakyReLU(),
                                            nn.Linear(self.hidden_size,n_classes))
            else:
                self.layer1 = nn.Sequential(nn.Dropout(0.2),
                                            nn.Linear(self.input_size, self.hidden_size),
                                            nn.LeakyReLU(),
                                            nn.Linear(self.hidden_size,self.hidden_size),
                                            nn.LeakyReLU(),
                                            nn.Linear(self.hidden_size,self.hidden_size),
                                            nn.LeakyReLU(),
                                            nn.Linear(self.hidden_size,n_classes))
                    
                                        
        def forward(self, input_sample):
            intermediate = self.layer1(input_sample)
            out = F.log_softmax(intermediate)
            return out


    def get_website():
        return 'https://en.wikipedia.org/wiki/Multilayer_perceptron'
    
    def get_name():
        return "multilayer perceptron"
    
    def get_category():
        return "perceptron"
    
    def get_class_name():
        return "MLP"
    
    
    def preprocess(data):
        
        if data.data_type == 'image':
            return np.asarray(data.data)/255
        if data.data_type == 'numeric':
            return StandardScaler().fit_transform(np.asarray(data.data))


    def train(data):
    
        combined_data = list(zip(data.data,data.labels))
        random.shuffle(combined_data)
        all_data,all_labels = zip(*combined_data)
        train_data, train_labels = all_data[0:int(len(all_data)*0.8)],all_labels[0:int(len(all_labels)*0.8)]
        test_data, test_labels = all_data[int(len(all_data)*0.8):len(data)],all_labels[int(len(all_labels)*0.8):len(all_labels)]
        
        time_constraint = data.time_constraint

        if time_constraint == 1:
          model = MLP.Perceptron(len(data.data[0]),len(data.data[0]),len(set(data.labels)))
          loss_function = nn.CrossEntropyLoss()
          optimizer = optim.SGD(model.parameters(),lr=1)
          n_epochs = 5
                    
        if time_constraint == 2:
            model = MLP.Perceptron(len(data.data[0]),100,len(set(data.labels)))
            loss_function = nn.CrossEntropyLoss()
            optimizer = optim.SGD(model.parameters(),lr=0.01)
            n_epochs = 5
                            
        if time_constraint == 3:
            model = MLP.Perceptron(len(data.data[0]),100,len(set(data.labels)))
            loss_function = nn.CrossEntropyLoss()
            optimizer = optim.ADAM(model.parameters())
            n_epochs = 10

        if time_constraint == 4:
            model = MLP.Perceptron(len(data.data[0]),100,len(set(data.labels)))
            loss_function = nn.CrossEntropyLoss()
            optimizer = optim.ADAM(model.parameters())
            n_epochs = 20
                                            
        if time_constraint == 5:
             model = MLP.Perceptron(len(data.data[0]),100,len(set(data.labels)),extratime=True)
             loss_function = nn.CrossEntropyLoss()
             optimizer = optim.ADAM(model.parameters())
             n_epochs = 50
                                                    
                                                    
        ''' TODO: blind data'''
        blind_data = None
        if data.prior_test_data is not None:
           train_data, train_labels = all_data,all_labels
           test_data = data.prior_test_data
           train_net(train_data, train_labels)
           

def train_net(train_data,train_labels,test_data,test_labels,model,optimizer,loss_f,n_epochs):
    
    batches = batchify(train_data,train_labels)
    
    
    for epoch in range(n_epochs):
        model.train()
        for n,batch in enumerate(batches[0:1000]):
            cells = batch[0]
            lbls = batch[1]
            pred = model(torch.Tensor(cells).view(16,len(train_data[0])))
            model.zero_grad()
            _,predicted = torch.max(pred.data,1)
            loss = loss_f(pred,torch.Tensor(lbls))
            loss.backward()
            optimizer.step()
    return model


def validate(model,test_data,test_labels=None):
    
    if test_labels == None:
        test_batches = batchify(test_data,[-1 for i in range(len(test_data))],size = 1)    
    else:
        test_batches = batchify(test_data,test_labels,size = 1)                                                  
    ####VALIDATION
    model.eval()
    all_preds = []
    with torch.no_grad():
        correct = 0
        total = 0
        for batch in test_batches:
           for cell,label in batch:
               outputs = model(torch.from_numpy(np.asarray([cell])))
               _, predicted = torch.max(outputs.data, 1)
               if predicted == label:
                   correct += 1
               total+=1
        return correct/total
    
    

def batchify(data,labels,size=16):
    
    k = 0
    ls = []
    allb = []
    lbls = []
    
    for n,i in enumerate(data):
        ls.extend(torch.from_numpy(np.asarray(data[n])))
        lbls.append(labels[n])
        k += 1
        if k == size:
            allb.append((ls,lbls))
            ls = []
            lbls = []
            k = 0

    return allb
