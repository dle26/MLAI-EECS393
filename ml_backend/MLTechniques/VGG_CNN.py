import torch 
import torch.nn as nn
import torch.optim as optim
import pickle
import random
import numpy as np
import torch.nn.functional as F



'''' VGG-16 CNN architecture '''

class VGG_CNN:
    
    CUSTOM = True #smoothing via max pooling
    TECHNIQUE_TYPE = "supervised"
    
    class ConvNet(nn.Module):
    
    ###TODO: ADD Params for time customization (use SVM Class as template) + dual purpose, images+text
      def __init__(self,vocab_size,n_classes,dim,maxsize,isText=False):
        
        super(VGG_CNN.ConvNet, self).__init__()
        
        self.embeddings = nn.Embedding(vocab_size,dim)
        
        ### TODO: UPDATE ARCHITECTURE
        #### TODO: DETERMINE IDEAL # OF EPOCHS
        #### TODO: OPTIMIZED LR ADJUSTMENTS?
        
        
        self.layer1 = nn.Sequential(
            nn.Conv1d(1, 64, kernel_size=9, stride=1, padding=1),
            nn.BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True),
            nn.ReLU(),
            nn.Conv1d(64, 64, kernel_size=9, stride=1, padding=1),
            nn.BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Conv1d(64, 128, kernel_size=9, stride=1, padding=1),
            nn.BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True),
            nn.ReLU(),
            nn.Conv1d(128, 128, kernel_size=9, stride=1, padding=1),
            nn.BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2))
        
         
        self.classifier = nn.Sequential(
          nn.Linear(2048,4096),
          nn.Dropout(),
          nn.Linear(4096,4096),
          nn.ReLU(),
          nn.Dropout(),
          nn.Linear(4096, n_classes))
    
 
##TODO: reformat for IMAGES 
        
    def forward_for_images(self, x):
        pass
    
    
    def forward_for_text(self,x):
        
        out = torch.from_numpy(x).long()
     
        out = self.embeddings(out)

        out = out.view(len(x), 1, -1)
       
        out = self.layer1(out)

        out = out.reshape(out.size(0), -1)
        out = out.view(35, 1, 2048)
        out = self.classifier(out.flatten())
    
        out = F.log_softmax(out)

        return out

    
    def __init__(self):
        self.model = None
 

    def get_name():
        return 'vgg-16 cnn'
    
    def get_category():
        return 'cnn'
    
    def get_general_category():
        return 'deep learning'
    
    def train(self,data,time_constraint):
    
        ###TODO: IMPLMEMENT THESE  + ADD TIME CONSTRAINTS
        model = None
        loss_function = None
        optimizer = None
        epochs = 0
        test_ln = None
        test = None
        
        train = data.data
        train_ln = data.train_labels

        batches = batchify(train,train_ln)    
        test_batches = batchify(test,test_ln,size = 1) 
        
        all_results = {}
        for k in np.unique(train_ln):
            all_results[k] = [0,0]

        for epoch in range(epochs):
            model.train()  
            total = 0
            correct = 0
            for n,batch in enumerate(batches):
                model.zero_grad()
                
                for item,label in batch:
                    pred = model(item)
                    _, predicted = torch.max(pred.data,1)
                    if (predicted == label):
                        correct += 1
                        all_results[label][0] += 1
                    all_results[label][1] += 1
                    total += 1
                    label = torch.LongTensor([label])
                    loss = loss_function(pred,label)
                    loss.backward()
                    optimizer.step()
         
        model.eval()
        
        results = []
        
        with torch.no_grad():
            correct = 0
            total = 0
            for sentence, label in test_batches:
                outputs = model(sentence)
                _, predicted = torch.max(outputs.data, 1)
                results.append(predicted)
                correct += (predicted == label).sum().item()

     
        data.prediction_results = (results,VGG_CNN.get_name())
        data.current_models.extend((self,VGG_CNN.get_name()))
        data.feat_importances.extend((None,VGG_CNN.get_name()))
  
    


###UTIL METHOD

def batchify(data,labels,size=16):

    k = 0
    ls = []
    allb = []
    for n,i in enumerate(data):
        ls.append((data[n],labels[n]))
        k += 1
        if k == size:
            allb.append(ls)
            ls = []
            k = 0 
            
    return allb
