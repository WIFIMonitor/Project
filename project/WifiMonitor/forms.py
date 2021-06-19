from django import forms
from .models import Departments

class DateInput(forms.DateInput):
    input_type = 'date'	

class DateForm(forms.Form):
    start = forms.DateField(widget=DateInput)
    end = forms.DateField(widget=DateInput)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start')
        end_date = cleaned_data.get('end')

        if(start_date != None and end_date!=None):
            if(end_date < start_date):
                raise forms.ValidationError(('end_date error'))

        return cleaned_data

class IntentionForm(forms.Form):
    departs = forms.ModelChoiceField(queryset=Departments.objects.all().order_by('name'),label="",required=False,empty_label="Departamento")

class SpecificBuildingForm(forms.Form):
    start = forms.DateField(widget=DateInput)
    end = forms.DateField(widget=DateInput)
    departs = forms.ModelChoiceField(queryset=Departments.objects.all().order_by('name'),label="",required=False,empty_label="Departamento")


