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

