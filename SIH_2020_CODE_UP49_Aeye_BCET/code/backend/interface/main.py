'''
file name : main.py
'''

from backend.data import driver as dataDriver
from backend.model import driver as modelDriver
from backend.model.model import create
from tqdm import tqdm

from tensorflow import keras

import pandas as pd
import glob

class Forecast:

    def __init__(self, patientData):

        
        
        data = [file for file in glob.glob(patientData+"*.psv")]
        self.threshold = 0.5

        for file in data :
            df = pd.read_csv(file,sep='|')
            df['Id'] = 1        
            patientData,_ = dataDriver.preprocess(df,trainingData=False)
            data = self._hourly(patientData[0])
            self.patientData = modelDriver.generateData(data)
            predictions = model.predict(self.patientData)
            
            predict = [x[0] for x in predictions]
            predictions2 = [1 if x > 0.5 else 0 for x in predict]
           
            df2 = {"PredictedProbability":predict, "PredictedLabel" : predictions2}
            df2 = pd.DataFrame(df2)
            df2.to_csv('Backend/NewFolder/' +file.strip("/Backend/Data/Datasets/TestSet_Day1") ,sep='|',index=False)

    
    def _hourly(self,patientData):

        data = []
        for hour in range(len(patientData)):

            data.append(patientData[0:hour+1])

        return data            






if __name__ == '__main__':

        model = create(-10.0)
        print("Loading Trained Model . . ")
        model.load_weights("Backend/Model/saved/")

        obj  = Forecast("Backend/Data/Datasets/TestSet_Day1/")

        


