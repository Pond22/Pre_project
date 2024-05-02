from django import forms
from .models import *

class Form(forms.ModelForm):
    class Meta:
        model = Form
        fields = ("name", "id")

class Plo_form(forms.ModelForm):
    class Meta:
        model =Teamplates
        fields = ("semester", "year_number")

