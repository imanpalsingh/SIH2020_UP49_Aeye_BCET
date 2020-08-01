'''
file name : driver.py 
'''

from backend.data import loader,preprocessor


import pandas as pd
import numpy as np


def loadData(filename : str,savePath='Backend/Data/Datasets/combinedData.csv',training_data = True) -> None:
    

    sep = loader.Loading(filename,verbose=True,training_data=training_data)
    sep.save(savePath)
    


def preprocess(df : pd.core.frame.DataFrame, trainingData : bool = True) -> None :
    
  

    sep = preprocessor.Common(df,verbose=trainingData)   
    sep.impute() 
    sep.oneHotEncode('Gender',trainingData)
    
    
    sep = preprocessor.FeatureEngineering(sep.dataset)
    sep.addSofa()
    sep.addShockIndex()
    
    
   
    sep = preprocessor.Tensor(sep.dataset,createLabels = trainingData,verbose=trainingData)
    if trainingData:
        sep.save('Backend//Data//Datasets//Tensor.npz')

    else:
        return np.array(sep.dataset),sep.columns[1:]   
       

if __name__ == "__main__":
    
    loadData('Backend/Data/Datasets/Raw/') 
    df = pd.read_csv("Backend/Data/Datasets/combinedData.csv")
    preprocess(df)

    
    
    
    
    
    
    
    
    
    
