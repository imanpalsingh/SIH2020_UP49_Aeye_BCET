'''
file name : main.py
'''

from backend.data import driver as dataDriver
from backend.model import driver as modelDriver
from backend.model.model import create
from tqdm import tqdm

from tensorflow import keras
import json
import pandas as pd
import glob

class Forecast:

    def __init__(self, patientData,asynchro = False,to_json=False):

        

        if asynchro:

            if patientData.endswith('.psv'):
                df = pd.read_csv(patientData,sep='|')
                df['Id'] = 1
                prob,labels = self.compute(df)

                if to_json:

                    patientname = str(patientData.replace("backend/interface/test_data\\",""))
                    patientname = str(patientname.replace(".psv",""))
                    
                    new_params = { ""+patientname : labels }
                    with open("Backend/interface/test_result/result.json",'r',encoding='utf-8') as file:
                        
                        params = json.load(file)

                    with open("Backend/interface/test_result/result.json",'w',encoding='utf-8') as file:
                        params.update(new_params)
                        json.dump(params,file,indent=2)

                    print("saved")
                else:

                    self.save(patientData,prob,labels)
                    
                    

        elif isinstance(patientData,str):
            
            data = [file for file in glob.glob(patientData+"*.psv")]
            self.threshold = 0.5

            for file in data :
                df = pd.read_csv(file,sep='|')
                df['Id'] = 1        
                probs,labels = self.compute(df)
                self.save(file,probs,labels)
        
        elif isinstance(patientData,dict):

            df = pd.DataFrame({k: pd.Series(l) for k, l in patientData.items()})
            df['Id'] = 1
            _,self.labels = self.compute(df)
        
            
    def save(self,filename,probs,labels):

        df2 = {"PredictedProbability":probs, "PredictedLabel" : labels}
        df2 = pd.DataFrame(df2)
        df2.to_csv('backend/interface/test_result/' +filename.replace("backend/interface/test_data\\","") ,sep='|',index=False)        
        print("File saved, just now")

    def get(self):

        return self.labels


    def compute(self,df):
        
        patientData = dataDriver.preprocess(df,trainingData=False)
        data = self._hourly(patientData[0])
        patientData = modelDriver.generateData(data)
        predictions = model.predict(patientData)
        predict = [x[0] for x in predictions]
        print(predict)
        predictions2 = [1 if x > 0.5 else 0 for x in predict]

        return predict, predictions2
            
    
    def _hourly(self,patientData):

        data = []
        for hour in range(len(patientData)):

            data.append(patientData[0:hour+1])

        return data  



if __name__ != '__main__':

        model = create(-10.0)
        print("Loading Trained Model . . ")
        model.load_weights("Backend/Model/saved/")
        print("Done")

        


