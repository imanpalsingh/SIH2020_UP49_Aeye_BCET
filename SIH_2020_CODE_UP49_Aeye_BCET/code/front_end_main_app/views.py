from django.shortcuts import render
from . forms import Patient_input_form
import datetime
from front_end_main_app.models import pt_data
from django.core import mail
from backend.interface.main import Forecast
import json
import numpy as np


# Create your views here.

#function for rendering the Homepage(index.html)
def index(request):
	return render(request,'index.html')

def patientForm(request):
    form=Patient_input_form()
    return render(request,'user_input_for_prediction.html',{'form': form })


def status(request):


    # If new file is created, a new json file will be created in backend/interface/test_result
    # read the json file from here
    with open("Backend/interface/test_result/result.json",'r') as file:
            params = json.load(file)
    
    # params is the dictionary which has structure as follows
    '''
    {
    "p100008.psv": [1,1,1,1,1,1,1,1,]


    '''
    context={'params':params}
    
    return render(request,'status.html',context)



def  result(request):
    if request.method=="POST":
        pk=request.POST.copy()
    
    pt_values=pt_data.objects.values()
    patientData = pt_values[0]


    Id = patientData.pop('Patient_id')


    convertStringToList(patientData)

    obj = Forecast(patientData)
    output = obj.get()


    
    context={'pt_values':pt_values ,'output':output}

    return render(request,'result.html',context)


def convertStringToList(dictionary):
    '''
    Function to convert a dictionary of strings to dictionary of lists

    Input
    =====

    `dictionary` : `dict`

    dictionary to convert

    Output
    ======
    `None`

    Example
    =======

    >>> convertStringToList(patientData)

    THe dictionary like `{ 'HR' : '1,2,3,4' , 'SBP' : '1,2,3,4' }`

    will be converted to required format as

    `{ 'HR' : [1,2,3,4] , '
    SBP' : [1,2,3,4] }`

    '''
    for key in dictionary.keys():
        
        values = []
        for val in dictionary[key].split(','):

            if val == 'None':
                continue
               

            elif val != ' None':
                values.append(float(val))

        dictionary[key] = values



