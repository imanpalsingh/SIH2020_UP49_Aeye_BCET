from django import forms

#this is user input form which will take values from user
class Patient_input_form(forms.Form):
    
    Patient_id = forms.CharField(label="Patient Id", max_length=100, required=False)