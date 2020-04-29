import torch 
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
import torch.nn.functional as F
from sklearn.preprocessing import StandardScaler


'''' VGG-16 CNN architecture '''

class VGG_CNN:
    
    TECHNIQUE_TYPE = "supervised"
    ISDEEP = True
    
    class ConvNet(nn.Module):
    
      def __init__(self,feature_len,dim,n_classes):
        
        super(VGG_CNN.ConvNet, self).__init__()
    
        self.n_classes = n_classes
        
        self.layer1 = nn.Sequential(
            nn.Conv1d(1, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True),
            nn.ReLU(),
            nn.Conv1d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Conv1d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True),
            nn.ReLU(),
            nn.Conv1d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2))
        

    

      def forward(self, x):
        

        x =x.view(len(x), 1, -1)

        x = self.layer1(x)

        x = x.view(x.size(0), -1)
        clf = nn.Sequential(nn.Linear(x.shape[1],4096),
        nn.Dropout(),
        nn.Linear(4096,4096),
        nn.ReLU(),
        nn.Dropout(),
        nn.Linear(4096, self.n_classes))
    
        x = clf(x)

        x = F.log_softmax(x)
   
        return x

    

    def get_name():
        return 'vgg_16 cnn'
    
    def get_category():
        return 'cnn'
    
    def get_class_name():
        return 'VGG_CNN'
    
    
    def get_website():
        return 'https://en.wikipedia.org/wiki/Convolutional_neural_network'
    

    def preprocess(data):

        if data.data_type == 'image':
            features = np.asarray(data.data)/255
            if data.prior_test_data is not None:
                 test_features = np.asarray(data.prior_test_data)/255
                 return features, test_features
            return features,None
        
                
        if data.data_type == 'numeric':
            features = StandardScaler().fit_transform(data.data)
            if data.prior_test_data is not None:
                test_features = StandardScaler().fit_transform(data.prior_test_data)
                return features,test_features
            return features,None
        
 

    def train(data):
    
        
        X,Xtest = VGG_CNN.preprocess(data)
        
        combined_data = list(zip(X,data.labels))
        random.shuffle(combined_data)
        all_data,all_labels = zip(*combined_data)
        train_data, train_labels = all_data[0:int(len(all_data)*0.8)],all_labels[0:int(len(all_labels)*0.8)]
        test_data, test_labels = all_data[int(len(all_data)*0.8):len(all_data)],all_labels[int(len(all_labels)*0.8):len(all_labels)]
         
        
        time_constraint = data.time_constraint
                               
                    
        if time_constraint == 2:
      
            model =  VGG_CNN.ConvNet(len(train_data[0]),len(data.data[0]),len(set(data.labels)))
            loss_function = nn.CrossEntropyLoss()
            optimizer = optim.SGD(model.parameters(),lr=0.01)
            n_epochs = 5
            model = train_net(train_data,train_labels,test_data,test_labels,model,optimizer,loss_function,n_epochs)
            results = validate(model,test_data)
                                                    
                            
        if time_constraint == 3:
            model =  VGG_CNN.ConvNet(len(train_data[0]),100,len(set(data.labels)))
            loss_function = nn.CrossEntropyLoss()
            optimizer = optim.Adam(model.parameters())
            n_epochs = 10
            model = train_net(train_data,train_labels,test_data,test_labels,model,optimizer,loss_function,n_epochs)
            results = validate(model,test_data)
                                                    

        if time_constraint == 4:
            model =  VGG_CNN.ConvNet(len(train_data[0]),100,len(set(data.labels)))
            loss_function = nn.CrossEntropyLoss()
            optimizer = optim.Adam(model.parameters())
            n_epochs = 20
            model = train_net(train_data,train_labels,test_data,test_labels,model,optimizer,loss_function,n_epochs)
            results = validate(model,test_data)
                                                    
                                            
        if time_constraint == 5:
             model =  VGG_CNN.ConvNet(len(train_data[0]),100,len(set(data.labels)),extratime=True)
             loss_function = nn.CrossEntropyLoss()
             optimizer = optim.Adam(model.parameters())
             n_epochs = 50
             model = train_net(train_data,train_labels,test_data,test_labels,model,optimizer,loss_function,n_epochs)
             results = validate(model,test_data)
                                                    
                                                    
        ''' TODO: blind data'''
        blind_results = None
         
        if data.prior_test_data is not None:
           train_data, train_labels = all_data,all_labels
           test_data = data.prior_test_data
           model = train_net(train_data, train_labels)
           blind_results = validate(model,Xtest)
           
    
        return test_data,test_labels,results,None, blind_results
           
        
        

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
            loss = loss_f(pred,torch.LongTensor(lbls))
            loss.backward()
            optimizer.step()

    return model


def validate(model,test_data):
    

    test_batches = batchify(test_data,[-1 for i in range(len(test_data))],size = 1)    
                                              
    ####VALIDATION
    model.eval()
    all_preds = []
    with torch.no_grad():
      for batch in test_batches:
          cells = batch[0]
          outputs = model(torch.Tensor([cells]))
          _, predicted = torch.max(outputs.data, 1)
          all_preds.append(predicted)

    return all_preds

    
    

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
