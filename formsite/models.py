from django.db import models
from django.contrib.auth.models import User, AbstractUser
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
# Create your models here.

'''
user_fields = User._meta.fields

for field in user_fields:
    print(field.name)       #related_name สำคัญ
    class Departments(models.Model):
    name = models.CharField(max_length=100)
'''
class Departments(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
      
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, null=True, blank=True, on_delete=models.CASCADE)
    line_token = models.CharField(max_length=45, null=True, blank=True)
    prefix = models.CharField(max_length=10, blank=True, verbose_name='คำนำหน้าชื่อ')

    def __str__(self):
        return self.user.username
    
class Teamplates(models.Model):
    id = models.BigAutoField(primary_key=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    semester_choices = (
        (1, '1'),
        (2, '2'),
        (3, '3')
    )
    semester = models.IntegerField(choices=semester_choices)
    year_number = models.IntegerField(
        verbose_name='ปี', 
        help_text='ใส่ตัวเลขปี 4 ตัว',
        validators=[MinValueValidator(2567), MaxValueValidator(2570)]
    )
    
    def save(self, *args, **kwargs):
        if self.is_active:
            active_forms_count = Teamplates.objects.filter(is_active=True, semester=self.semester, year_number=self.year_number).count() #ตรวจ active
            if active_forms_count > 0:
                self.is_active = False
        
        return super().save(*args, **kwargs)
    
class TemplateData(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_items')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    form = models.ForeignKey(Teamplates, on_delete=models.CASCADE, related_name='TemplateData')
    
    def __str__(self):
        return f"{self.text} ({self.id})"
    
class CLO(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_items')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    form = models.ForeignKey(Teamplates, on_delete=models.CASCADE, related_name='CLO')
    
    def __str__(self):
        return f"{self.text} ({self.id})"

class Course(models.Model):
    teamplates = models.ForeignKey(Teamplates, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    """ section = models.CharField(max_length=2) """
    class_code = models.CharField(max_length=7)

class Section(models.Model):
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)
    session_number = models.IntegerField()

    def __str__(self):
        return f"{self.course.name} - ตอนเรียนที่ {self.session_number} ~ ID = {self.id}"
    

class Form(models.Model):
    semester_choices =(
        #("Undefined","Undefined"),
        (1, '1'),
        (2, '2'),
        (3, '3')
    )
    
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='forms')
    
    name = models.CharField(max_length=100)
    class_code = models.CharField(max_length=10)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='forms')
 
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    create = models.DateTimeField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    template = models.ForeignKey(Teamplates, on_delete=models.CASCADE)
    is_teacher_form = models.BooleanField(default=False)
    """ year_number = models.IntegerField(
        verbose_name='ปีการศึกษา', 
        validators=[MinValueValidator(1999), MaxValueValidator(3100)]
    ) """           
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    expired = models.BooleanField(default=False) #เก็บว่าแบบฟอร์มนั้นครบกำหนดเวลาหรือยัง
    #users = models.ManyToManyField(User, related_name='forms') #ทำให้เกี่ยวกันกับ User แบบ M to N 
     
    def __str__(self):
        return f"ไอดีฟอร์ม {self.id} secID {self.section.id}"
 
class AuthorizedUser(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)  
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
    def __str__(self):
        return f"ฟอร์มที่ = {self.form.id} Username = {self.users.username}"
    
class AssessmentItem(models.Model):    
    text = models.TextField()
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    template_select = models.ForeignKey(TemplateData, on_delete=models.CASCADE,null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_items')
    id = models.BigAutoField(primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.template_select:
            return f"มากจากแม่แบบ ID = {self.id} ข้อมูล = {self.template_select.text}"    #self.template_select.text
        else:
            return f"มากจากฟอร์ม = {self.form} ID = {self.id}"

class CommentForm(models.Model):
    id = models.BigAutoField(primary_key=True)
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    form = models.ForeignKey(Form, related_name="comments", on_delete=models.CASCADE)
    
        
class AssessmentResponse(models.Model):
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    response_date = models.DateTimeField(auto_now_add=True)
    assessment_item  = models.ForeignKey(AssessmentItem, on_delete=models.CASCADE)
    response = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    def __str__(self):
        return f"มาจากคำถามไอดีที่ {self.assessment_item.id} ของฟอร์มที่ {self.assessment_item.form.id} คนตอบ {self.respondent}"
    

    

