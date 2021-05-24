from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'	

class DateForm(forms.Form):
     start = forms.DateField(widget=DateInput)
     end = forms.DateField(widget=DateInput)
