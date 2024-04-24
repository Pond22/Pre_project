from django import forms
from .models import *

class Form(forms.ModelForm):
    class Meta:
        model = form
        fields = ("name", "id")

class Plo_form(forms.ModelForm):
    class Meta:
        model =Form_plos
        fields = ("school_year", "year_number")

