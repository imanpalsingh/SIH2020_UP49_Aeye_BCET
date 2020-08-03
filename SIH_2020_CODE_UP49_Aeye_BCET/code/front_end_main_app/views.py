from django.shortcuts import render
from . forms import Patient_input_form
import datetime
from models import dbms1
from django.core import mail


# Create your views here.

#function for rendering the Homepage(index.html)
def index(request):
	return render(request,'index.html')

def patientForm(request):
    form=Patient_input_form()
    return render(request,'user_input_for_prediction.html',{'form': form })


def result(request):
    if request.method == "POST":
        user_input_values = request.POST.copy()
    patientData = user_input_values.dict()
    # Deleting the metdata in the dictionary as it is not required
    del patientData['csrfmiddlewaretoken']

    Name = patientData.pop('Patient_name')
    Id = patientData.pop('Patient_id')

    # Converting the values that are as a string to lists
    convertStringToList(patientData)
    output="output"
    # if output > 0.5:
    #   connection = mail.get_connection()
    #  connection.open()
    # email = mail.EmailMessage(
    #    'Sepsis Detected !',
    #   'Patient : ' + Name + '\nPatient Id : ' + Id + '\nSepsis Result : Positive',
    #  'nandan980633@gmail.com',
    # ['imanpalsingh@gmail.com'],
    # )
    # connection.send_messages([email])
    # connection.close()
    temp = dbms1(pt_id=Id, pt_name=Name, pt_output=output, created_at=datetime.datetime.now())
    temp.save()
    db=dbms1.objects.get.all()
    context = {'db': db, 'output': output, 'pt_name': Name, 'pt_id': Id, 'created_at': datetime.datetime.now()}
    return render(request, 'result_ml.html', context)


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

    `{ 'HR' : [1,2,3,4] , 'SBP' : [1,2,3,4] }`

    '''
    for key in dictionary.keys():
        values = [float(val) for val in dictionary[key].split(',')]
        dictionary[key] = values



