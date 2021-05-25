from django import forms
from .models import Departments

class DateInput(forms.DateInput):
    input_type = 'date'	

class DateForm(forms.Form):
     start = forms.DateField(widget=DateInput)
     end = forms.DateField(widget=DateInput)

class IntentionForm(forms.Form):
    departs = forms.ModelChoiceField(queryset=Departments.objects.all().order_by('name'),label="",required=False)

