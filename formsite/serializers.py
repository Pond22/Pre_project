from rest_framework import serializers
from .models import *
from django import forms
from django.contrib.auth.models import User
import re

class Form(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ("name", "id")
        
        
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@payap\.ac\.th$'
    return re.match(pattern, email) is not None
        
class CSVUploadForm(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not validate_email(email):
            raise forms.ValidationError("Invalid email format. Please enter a valid email address with domain payap.ac.th.")
        return email
    csv_file = forms.FileField(label='อัปโหลดไฟล์ CSV')
    