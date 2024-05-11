from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.core.validators import EmailValidator
from formsite.models import User as CustomUser

#regex 
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@payap\.ac\.th$'
    return re.match(pattern, email) is not None
    
class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not validate_email(email):
            raise forms.ValidationError("Invalid email format. Please enter a valid email address with domain payap.ac.th.")
        return email