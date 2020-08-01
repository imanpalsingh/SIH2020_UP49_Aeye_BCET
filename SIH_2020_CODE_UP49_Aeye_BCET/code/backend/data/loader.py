'''
file name : loader.py 
'''
 

import pandas as pd

from tqdm import tqdm

import os
import glob


class Loading:
    
  
    def __init__(self,path : str, verbose: bool = False, training_data = True) -> None :
        
    
        self.path = None
        
        self.path = path
 
        self.verbose= verbose
        
        self.dataset = None

        self.training_data = training_data
        
        self._readFile()
        
    
    def _readFile(self) -> None :
        
        
        if self.training_data :
            data = [file for file in glob.glob(self.path+"/*/*.psv")]
        else:
             data = [file for file in glob.glob(self.path+"*.psv")]
 
        if self.verbose: 
            print("'{}' file names loaded from '{}'. ".format(str(len(data)),os.path.realpath(self.path)))
    
        
        combinedPatientData = []
        
        patientId = 0
        for file in (tqdm(data,desc="Accessing patient data ",ascii = ' |/-\|/-\#') if self.verbose else data) : 

                patientData = pd.read_csv(file,sep='|')
                patientData.insert(0,'Id',patientId)
                patientData.fillna(method='ffill',axis='rows',inplace=True)
                patientData.fillna(method='bfill',axis='rows',inplace=True)
                combinedPatientData.append(patientData)
                patientId+=1
            
            
        self.dataset = pd.concat(combinedPatientData)            
       
    def save(self,filepath):
   
        self.dataset.to_csv(filepath,index=False)
        if self.verbose: print("'{}' saved".format(filepath))
    


