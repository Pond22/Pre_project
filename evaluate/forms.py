from django import forms
from formsite.models import TemplateData, Form, AssessmentItem, Course, Section
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.forms import DateTimeInput
from django.utils import timezone
from django.core.exceptions import ValidationError

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class PLOsForm(forms.ModelForm):
    class Meta:
        model = TemplateData
        fields = ['text']
        
class FormUpdateForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = [
            'section',
            'start_date',
            'end_date',
            'description',
        ]
        widgets = {
            'section': forms.Select(choices=()),
            #'section': forms.Select(choices=((1, 'ตอนเรียนที่ 1'), (2, 'ตอนเรียนที่ 2'), (3, 'ตอนเรียนที่ 3'), (4, 'ตอนเรียนที่ 4'), (5, 'ตอนเรียนที่ 5'), (6, 'ตอนเรียนที่ 6'), (7, 'ตอนเรียนที่ 7'), (8, 'ตอนเรียนที่ 8'), (9, 'ตอนเรียนที่ 9'), (10, 'ตอนเรียนที่ 10'))),
            'start_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'class': 'form-control'}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['section'].queryset = Section.objects.filter(course=self.instance.course)

class Assessment_Form(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['course', 'section', 'start_date', 'end_date', 'description', 'template']
        
        widgets = {
            'semester': forms.Select(choices=((1, '1'), (2, '2'), (3, '3'))),
            'section': forms.Select(choices=()),
            #'section': forms.Select(choices=((1, 'ตอนเรียนที่ 1'), (2, 'ตอนเรียนที่ 2'), (3, 'ตอนเรียนที่ 3'), (4, 'ตอนเรียนที่ 4'), (5, 'ตอนเรียนที่ 5'), (6, 'ตอนเรียนที่ 6'), (7, 'ตอนเรียนที่ 7'), (8, 'ตอนเรียนที่ 8'), (9, 'ตอนเรียนที่ 9'), (10, 'ตอนเรียนที่ 10'))),
            'start_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
        exclude = ['template'] 
           
    def __init__(self, *args, custom_param=None, **kwargs):
        super().__init__(*args, **kwargs)
        print(custom_param)
        courses = Course.objects.filter(teamplates=custom_param)
        c_choices = [('', 'เลือกรายวิชา')] + [(c.id, f'{c.class_code} | {c.name}') for c in courses]
        self.fields['course'].widget = forms.Select(choices=c_choices)
        self.fields['course'].label = 'รายวิชา'
        self.fields['start_date'].label = 'วันเวลาเริ่มต้นการประเมิน'
        self.fields['end_date'].label = 'วันเวลาสิ้นสุดการประเมิน'
        
        self.fields['section'].queryset = Section.objects.none()

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['section'].queryset = Section.objects.filter(course_id=course_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['section'].queryset = self.instance.course.sections.all()
        
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
    
    
LIKERT_CHOICES = [
    (1, ''),
    (2, ''),
    (3, ''),
    (4, ''),
    (5, ''),
]

class DynamicLikertForm(forms.Form):
    def __init__(self, *args, custom_param=None, **kwargs):
        super(DynamicLikertForm, self).__init__(*args, **kwargs)
        if custom_param:
            questions = AssessmentItem.objects.filter(form=custom_param, parent__isnull=True, template_select__isnull=True)
            for question in questions:
                # เพิ่มคำถามหลักในฟอร์มแบบไม่ต้องการคำตอบ
                self.fields[f'question_{question.id}'] = forms.CharField(
                    label=f"{question.text}",
                    #initial=question.text,
                    required=False,
                    widget=forms.TextInput(attrs={'disabled': 'disabled', 'style': 'border: none; background-color: transparent;', 'class': 'text-input-disabled'})
                )
                # ดึงคำถามย่อย
                sub_questions = question.sub_items.all()
                for sub_question in sub_questions:
                    self.fields[f'sub_question_{sub_question.id}'] = forms.ChoiceField(
                        label=f"{sub_question.text}",
                        choices=LIKERT_CHOICES,
                        widget=forms.RadioSelect(attrs={'class': 'radio-select'})
                    )
                    
            template_questions = AssessmentItem.objects.filter(form=custom_param, parent__isnull=True, template_select__isnull=False)
            for template_question in template_questions:
                # เพิ่มคำถามหลักจาก TemplateData ในฟอร์มแบบไม่ต้องการคำตอบ
                self.fields[f'template_question_{template_question.id}'] = forms.CharField(
                    label=f"{template_question.template_select.text}",
                    #initial=template_question.template_select.text,
                    required=False,
                    widget=forms.TextInput(attrs={'disabled': 'disabled', 'style': 'border: none; background-color: transparent;', 'class': 'text-input-disabled'})
                )
                # ดึงคำถามย่อยจาก TemplateData
                sub_template_questions = AssessmentItem.objects.filter(parent=template_question)
                for sub_template_question in sub_template_questions:
                    self.fields[f'template_sub_question_{sub_template_question.id}'] = forms.ChoiceField(
                        label=f"{sub_template_question.template_select.text}",
                        choices=LIKERT_CHOICES,
                        widget=forms.RadioSelect(attrs={'class': 'radio-select'})
                        
                    )

""" sub_template_questions = AssessmentItem.objects.filter(parent=template_question)
                for sub_template_question in sub_template_questions:
                    self.fields[f'template_sub_question_{sub_template_question.id}'] = forms.ChoiceField(
                        label=f"{sub_template_question.id} - {sub_template_question.template_select.text}",
                        choices=LIKERT_CHOICES,
                        widget=forms.RadioSelect(attrs={'class': 'radio-select'})
                        
                    ) """