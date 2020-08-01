'''
file name : creator.py
'''

import numpy as np


class Generator:
    
 
    def __init__(self,X,y=None,hoursPerPatient : int = 6, hoursToLookInFuture : int = 6, padValue : float = -10.0) -> None :
        
        self.hours = hoursPerPatient
        self.future = hoursToLookInFuture
        self.XStatic = []
        self.XTimeSeries = []
        self.padValue = padValue
        self.y = []
        
        self._create(X,y)
        
        
    def _create(self,X,y) -> None:
        
        if y is None:

            max_length = 0
            for index in range(len(X)):

                length = len(X[index])
                if length > max_length : max_length = length
            
            self.hours = max_length



        for patientIndex in range(len(X)):
            
            for observationIndex in range(0,len(X[patientIndex]),self.hours):
                
                patientData = X[patientIndex][observationIndex : observationIndex + self.hours]
                
                patientData[np.isnan(patientData)] = 0
                
                self.XStatic.append(patientData[-1,8:])
                if len(patientData) < self.hours:
                
                    paddedArray = np.full((self.hours - len(patientData),patientData.shape[1]),self.padValue)
                    patientData = np.r_[patientData,paddedArray]
                
                self.XTimeSeries.append(patientData[:,:8])
                
                if y is not None :
                    
                    if (observationIndex + self.hours + self.future - 1) >= len(y[patientIndex]):
                        
                        self.y.append(y[patientIndex][-1])
                        continue
                
                
                    self.y.append(y[patientIndex][observationIndex + self.hours + self.future -1])   
        
        self.XStatic = np.array(self.XStatic)
        self.XTimeSeries = np.array(self.XTimeSeries)
        self.y = np.array(self.y) 

    
    def get(self) -> None :

        return [self.XStatic,self.XTimeSeries] , self.y         
                
