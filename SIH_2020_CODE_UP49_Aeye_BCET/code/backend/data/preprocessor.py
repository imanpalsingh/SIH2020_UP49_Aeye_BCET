'''
file name : preprocessor.py
'''

import pandas as pd
pd.options.mode.chained_assignment = None 

from tqdm import tqdm

from sklearn.preprocessing import OneHotEncoder

import numpy as np

import os
from typing import Union

import pickle





class Common:
    
    
    def __init__(self,data :  pd.core.frame.DataFrame, verbose : bool = False) -> None :
        
        
        self.dataset = data
        self.verbose = verbose
        
        self.dataset.drop(['Unit1','Unit2'],inplace=True,axis=1,errors='ignore')
        
    
    def impute(self) -> None :
        
        self.dataset.fillna(self.dataset.mode(),inplace=True)
            
    
    
    def oneHotEncode(self,column : str , saveModel : bool = True) -> None :   
        

       
        
        if not saveModel:

            encoder = pickle.load(open("Backend/Data/Datasets/ohe.pkl",'rb'))
        
        if saveModel:

            encoder = OneHotEncoder(categories='auto',sparse=False)
            encoder.fit(self.dataset[column].values.reshape(-1,1))
            pickle.dump(encoder,open("Backend/Data/Datasets/ohe.pkl",'wb'))


        encoded = encoder.transform(self.dataset[column].values.reshape(-1,1)).T
        pos = self.dataset.columns.get_loc(column)
            
        col_num  = 0
        for col in range(len(encoded)-1,-1,-1):
            
            self.dataset.insert(loc=pos,column=column+str(col_num),value=encoded[col])
            pos += 1
            col_num += 1
            
        self.dataset.drop(column,axis='columns',inplace=True)
        
                          
    def save(self, filepath : str) -> None :
        
        self.dataset.to_csv(filepath,index=False)
        if self.verbose: print("'{}' saved".format(filepath))
        


class Tensor:
    
  
  def __init__(self,data :  pd.core.frame.DataFrame, createLabels : bool = True, verbose : bool = False,) -> None:
      
    self.dataset = []
    self.columns = data.columns
    self.verbose = verbose
    self.labels= []

    if createLabels:
        self._createLabels(data)

    self._create(data)
    
    
      
  def _create(self,data : pd.core.frame.DataFrame) -> None:
      
    
    data.drop(['SepsisLabel'],inplace=True, axis=1,errors='ignore')
    self.columns = data.columns
    
    patients = data['Id'].unique()
    
    for patientId in (tqdm(patients,desc="Creating Tensor",ascii = ' |/-\|/-\=') if self.verbose else patients):
      
      patientData = data[data['Id'] == patientId].drop('Id',axis='columns')
        
      self.dataset.append(patientData.values)
      
     
  def _createLabels(self,data : pd.core.frame.DataFrame) -> None:
     
  
   
   patients = data['Id'].unique()
   for patientId in (tqdm(patients,desc="Creating Labels",ascii = ' |/-\|/-\=') if self.verbose else patients):
      
     patientData = data[data['Id'] == patientId].drop('Id',axis='columns')

     self.labels.append(patientData['SepsisLabel'].values)
           
   self.labels = np.array(self.labels)


  def save(self,filepath : str) -> None:
   
    np.savez_compressed(filepath,X = self.dataset, y = self.labels , columns = self.columns[1:]) # Discarding the 'Id' columns
       


class FeatureEngineering:
    
  
    def __init__(self,data :  pd.core.frame.DataFrame) -> None:
        
        self.dataset  = data
    
    
    def addSofa(self) -> None:
        
        
        SOFA = np.zeros(len(self.dataset.index))
        
        MAP = self.dataset['MAP']
        SOFA[MAP >= 70] +=0
        SOFA[MAP < 70] +=1
        
        bilirubin = self.dataset['Bilirubin_total']
        SOFA[bilirubin < 1.2] += 0
        SOFA[(1.2 <= bilirubin) & (bilirubin <= 1.9)] += 1
        SOFA[(1.9 < bilirubin) & (bilirubin <= 5.9)] += 2
        SOFA[(5.9 < bilirubin) & (bilirubin <= 11.9)] += 3
        SOFA[bilirubin > 11.9] += 4
        
        platelets = self.dataset['Platelets']
        SOFA[platelets >= 150] += 0
        SOFA[(100 <= platelets) & (platelets < 150)] += 1
        SOFA[(50 <= platelets) & (platelets < 100)] += 2
        SOFA[(20 <= platelets) & (platelets < 50)] += 3
        SOFA[platelets < 20] += 4
        
        creatinine = self.dataset['Creatinine']
        SOFA[creatinine < 1.2] += 0
        SOFA[(1.2 <= creatinine) & (creatinine <= 1.9)] += 1
        SOFA[(1.9 < creatinine) & (creatinine <= 3.4)] += 2
        SOFA[(3.4 < creatinine) & (creatinine <= 4.9)] += 3
        SOFA[creatinine > 4.9] += 4
        
        self.dataset['SOFA'] = SOFA
        
        if 'SepsisLabel' in self.dataset.columns:
             # Making the SepsisLabel the last column
            self.dataset = self.dataset[[x for x in self.dataset.columns if  x not in ['SepsisLabel']] + ['SepsisLabel']]
        

    
   
    def addShockIndex(self):
        
        self.dataset['SI'] = self.dataset['HR'] / self.dataset['SBP']
        self.dataset['ModifiedSI'] = self.dataset['HR'] / (self.dataset['MAP'])
        
        if 'SepsisLabel' in self.dataset.columns:
            # Making the SepsisLabel the last column
            self.dataset = self.dataset[[x for x in self.dataset.columns if  x not in ['SepsisLabel']] + ['SepsisLabel']]
        
                            
    def save(self, filepath : str) -> None :
        

        self.dataset.to_csv(filepath,index=False)
        if self.verbose: print("'{}' saved".format(filepath))
