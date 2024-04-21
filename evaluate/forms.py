from django import forms
from formsite.models import PLOs, form, clo, AuthorizedUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class Aut(forms.ModelForm):
    class Meta:
        model = AuthorizedUser
        fields = []
class PLOsForm(forms.ModelForm):
    class Meta:
        model = PLOs
        fields = ['text']
        
class PLOstest(forms.ModelForm):
    class Meta:
        model = PLOs
        fields = []
        #widgets = {'test': forms.TextInput(attrs={'class': 'form-control'})}  
        
class Form(forms.ModelForm):
    class Meta:
        model = form
        fields = ['name', 'class_code', 'school_year', 'section', 'year_number'] 
        
class ClosForm(forms.ModelForm):
    class Meta:
        model = clo
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