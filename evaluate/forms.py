from django import forms
from formsite.models import TemplateData, Form, AssessmentItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.forms import DateTimeInput
from django.utils import timezone
from django.core.exceptions import ValidationError


class PLOsForm(forms.ModelForm):
    class Meta:
        model = TemplateData
        fields = ['text']
        
class PLOstest(forms.ModelForm):
    class Meta:
        model = TemplateData
        fields = []
        #widgets = {'test': forms.TextInput(attrs={'class': 'form-control'})}  

class Assessment_Form(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['name', 'class_code', 'semester', 'section', 'year_number', 'start_date', 'end_date', 'description']
        
        widgets = {
            'semester': forms.Select(choices=((1, '1'), (2, '2'), (3, '3'))),
            'year_number': forms.Select(choices=((2567, '2567'), (2568, '2568'), (2569, '2569'))),
            'start_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            
        } 
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['template'].widget = forms.HiddenInput() 
        
class ClosForm(forms.ModelForm):
    class Meta:
        model = AssessmentItem
        fields = ['text']
        
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@payap\.ac\.th$'
    return re.match(pattern, email) is not None

class CSVUploadForm(forms.Form):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not validate_email(email):
            raise forms.ValidationError("Invalid email format. Please enter a valid email address with domain payap.ac.th.")
        return email
    csv_file = forms.FileField(label='อัปโหลดไฟล์ CSV')