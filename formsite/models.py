from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

'''
# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=255)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_response = models.TextField

'''

# Create your models here.

class form(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    class_code = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    school_year_choices =(
        #("Undefined","Undefined"),
        (1, '1'),
        (2, '2'),
        (3, '3')
    )
    school_year = models.IntegerField(choices=school_year_choices)
    section = models.CharField(max_length=2)
    year_number = models.IntegerField(
        verbose_name='ปี', 
        help_text='ใส่ตัวเลขปี 4 ตัว',
        validators=[MinValueValidator(1999), MaxValueValidator(3100)]
    )
    
class clo(models.Model):    
    text = models.TextField()
    form = models.ForeignKey(form, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.BigAutoField(primary_key=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text

class UserEvaluation(models.Model):
    name = models.CharField(max_length=100)
    evaluation_date = models.DateField(auto_now_add=True)
    question = models.ForeignKey(clo, on_delete=models.CASCADE)


class PLOs(models.Model):
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text


