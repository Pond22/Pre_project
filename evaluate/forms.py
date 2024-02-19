from django import forms
from formsite.models import PLOs, form, clo

class PLOsForm(forms.ModelForm):
    class Meta:
        model = PLOs
        fields = ['text']  
        
class Form(forms.ModelForm):
    class Meta:
        model = form
        fields = ['created_by'] 
        
class ClosForm(forms.ModelForm):
    class Meta:
        model = clo
        fields = ['text']
