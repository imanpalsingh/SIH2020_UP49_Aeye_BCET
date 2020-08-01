from django.shortcuts import render
from . forms import Patient_input_form

# Create your views here.


def patientForm(request):
    form=Patient_input_form()
    return render(request,'user_input_for_prediction.html',{'form': form })
