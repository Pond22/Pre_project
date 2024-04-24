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

class students(models.Model):
    students_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=80)

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

class AuthorizedUser(models.Model):
    form = models.ForeignKey(form, on_delete=models.CASCADE)
    stu_list = models.CharField(max_length=10)
    def __str__(self):
        return self.stu_list
    
class clo(models.Model):    
    text = models.TextField()
    form = models.ForeignKey(form, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_items')
    id = models.BigAutoField(primary_key=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text

class FormResponse(models.Model):
    form = models.ForeignKey(form, on_delete=models.CASCADE)
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    response_date = models.DateTimeField(auto_now_add=True)
    clo_item  = models.ForeignKey(clo, on_delete=models.CASCADE)
    response_clo = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    
    def __str__(self):
        return self.clo_item
    
class Form_plos(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    school_year_choices = (
        (1, '1'),
        (2, '2'),
        (3, '3')
    )
    school_year = models.IntegerField(choices=school_year_choices)
    year_number = models.IntegerField(
        verbose_name='ปี', 
        help_text='ใส่ตัวเลขปี 4 ตัว',
        validators=[MinValueValidator(2567), MaxValueValidator(2570)]
    )

class PLOs(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField(null=False, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_items')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    update = models.DateTimeField(auto_now=True)
    form = models.ForeignKey(Form_plos, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

