'''
file name : driver.py
'''


from sklearn.utils.class_weight import compute_class_weight

import numpy as np

import json
from typing import Union

from backend.data.creator import Generator
from backend.model.model import create


def loadData(filepath):

    Data = np.load(filepath,allow_pickle=True)   
    return Data['X'],Data['y']

 
def scale(X,Xval = None,Xtest = None):

    with open("Backend/settings/parameters.json",'r') as file:
                params = json.load(file)
        
    if Xval is None or Xtest is None:
        
        mean,std = params['mean'],params['std']
        X = np.array([x - mean for x in X])
        X = np.array([x/std for x in X])
        return X

    else:
        
        mean = np.nanmean(np.vstack(X),axis=0)
        X = np.array([x - mean for x in X])

        std = np.nanstd(np.vstack(X),axis=0)
        X = np.array([x/std for x in X])

        
        Xval = np.array([x - mean for x in Xval])
        Xval = np.array([x/std for x in Xval])

        Xtest = np.array([x - mean for x in Xtest])
        Xtest = np.array([x/std for x in Xtest])

        parameters = {'mean' : mean.tolist(), 'std' : std.tolist()}

        with open("Backend/settings/parameters.json",'w',encoding='utf-8') as file:
                params.update(parameters)
                json.dump(params,file,indent=4)
        
        return X,Xval,Xtest
    
    

def createModel(X,y,Xval,yval,Xtest,ytest,saveModel = True):

    class_weights = compute_class_weight('balanced',classes = [0,1],y = y)
    class_weights = { index : class_weights[index] for index in range(len(class_weights))}
    
    model = create(maskValue = -10.0)
    history = model.fit(X,y,validation_data=(Xval,yval),epochs=1,class_weight=class_weights,batch_size=50)

    
    if saveModel:
        model.save('Backend/Model/saved/')
    
    model.evaluate(Xtest,ytest)
    
    return history

def generateData(X_,y_ = None):

    if y_ is None :

        X_= scale(X_)
        X_,_ = Generator(X_).get()

        return X_

    else : 
        
        with open("Backend/settings/parameters.json",'r') as file:
            params = json.load(file)

        totalSize = len(X_)
        trainTill = int(totalSize * params['trainPerc'])
        valTill = int((totalSize - trainTill) * params['valPerc'] + trainTill)

        print("Training till  :", trainTill)
        print("Validting till :",valTill)

        X,y = X_[:trainTill],y_[:trainTill]
        Xval,yval = X_[trainTill:valTill],y_[trainTill:valTill]
        Xtest,ytest = X_[valTill:],y_[valTill:]

        X,Xval,Xtest = scale(X,Xval,Xtest)

        hoursPerPatient = params["hoursPerPatient"]
        hoursToLookInFuture = params["hoursToLookInFuture"]

        X,y = Generator(X,y, hoursPerPatient,hoursToLookInFuture).get()
        Xval,yval = Generator(Xval,yval,hoursPerPatient,hoursToLookInFuture).get()
        Xtest,ytest = Generator(Xtest,ytest).get()

        return [X,y] , [Xval,yval], [Xtest,ytest]



if __name__ == "__main__":

    X_,y_ = loadData('Backend/Data/Datasets/Tensor.npz')
    train, val, test = generateData(X_,y_)
    history = createModel(X = train[0],y = train[1],Xval = val[0],yval = val[1],Xtest=test[0],ytest = test[1],saveModel=True)


