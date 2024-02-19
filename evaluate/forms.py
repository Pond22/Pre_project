from django import forms
from formsite.models import PLOs, form, clo

class PLOsForm(forms.ModelForm):
    class Meta:
        model = PLOs
        fields = ['text']  
        
class Form(forms.ModelForm):
    class Meta:
        model = form
        fields = ['name', 'class_code', 'school_year', 'section', 'year_number'] 
        
class ClosForm(forms.ModelForm):
    class Meta:
        model = clo
        fields = ['text']
