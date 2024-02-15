from django import forms
from formsite.models import PLOs

class PLOsForm(forms.ModelForm):
    class Meta:
        model = PLOs
        fields = ['text']  
