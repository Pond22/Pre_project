from django.db import models
from django.contrib.auth.models import User
import datetime

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    
class clo(models.Model):
    text = models.CharField(max_length=255)
    form = models.ForeignKey(form, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.BigAutoField(primary_key=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(clo, on_delete=models.CASCADE)
    user_response = models.TextField

class UserEvaluation(models.Model):
    user_name = models.CharField(max_length=50)
    evaluation_date = models.DateField(auto_now_add=True)
    answers = models.ManyToManyField(Answer)


class PLOs(models.Model):
    text = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text


class section(models.Model):
    school_year_choices =(
        #("Undefined","Undefined"),
        (1, '1'),
        (2, '2'),
    )
    year = models.IntegerField(default=datetime.datetime.now().year)
    school_year = models.IntegerField(choices=school_year_choices)


