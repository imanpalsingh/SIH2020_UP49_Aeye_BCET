from django.shortcuts import render
from . forms import Patient_input_form


# Create your views here.

#function for rendering the Homepage(index.html)
def index(request):
	return render(request,'index.html')

def patientForm(request):
    form=Patient_input_form()
    return render(request,'user_input_for_prediction.html',{'form': form })


