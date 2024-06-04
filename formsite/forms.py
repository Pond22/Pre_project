from django import forms
from .models import *
from django.forms import DateTimeInput

class Form(forms.ModelForm):
    class Meta:
        model = Form
        fields = ("name", "id")

class Plo_form(forms.ModelForm):
    class Meta:
        model =Teamplates
        fields = ("semester", "year_number", 'start_date', 'end_date')
        
        widgets = {
            'year_number': forms.Select(choices=((2567, '2567'), (2568, '2568'), (2569, '2569'))),
            'start_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True}),
    
        }
        
class UpdateTemplateForm(forms.ModelForm):
    class Meta:
        model = Teamplates
        fields=('start_date', 'end_date')
        
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True}),
        }
        
    def __init__(self, *args, **kwargs):
        start_date = kwargs.pop('start_date', None)
        end_date = kwargs.pop('end_date', None)
        super(UpdateTemplateForm, self).__init__(*args, **kwargs)
        if start_date:
            self.fields['start_date'].initial = start_date
        if end_date:
            self.fields['end_date'].initial = end_date

