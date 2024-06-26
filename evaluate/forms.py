from django import forms
from formsite.models import TemplateData, Form, AssessmentItem, Course, Section, Teamplates
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.forms import DateTimeInput
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class PLOsForm(forms.ModelForm):
    class Meta:
        model = TemplateData
        fields = ['text']
        
class FormUpdateForm(forms.ModelForm): #หน้าแก้ไขฟอร์ม
    class Meta:
        model = Form
        fields = [
            'section',
            #'start_date',
            #'end_date',
            'description',
        ]
        widgets = {
            'section': forms.Select(choices=()),
            'description': forms.Textarea(attrs={
                'rows':'4',
                'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 border-gray-500',}),
            #'start_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True, 'readonly': True}),
            #'end_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True, 'readonly': True}),
        }

    def __init__(self, *args, **kwargs):#แสดงตอนเรียนที่ไม่ซ้ำกับอันที่มีในระบบ
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            active_template = self.instance.template

            used_sections = Form.objects.filter(course=self.instance.course, template=active_template).exclude(id=self.instance.id).values_list('section_id', flat=True)
            current_section_id = self.instance.section.id if self.instance.section else None
            sections_filter = Q(course=self.instance.course) & (~Q(id__in=used_sections) | Q(id=current_section_id))
            self.fields['section'].queryset = Section.objects.filter(sections_filter)

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()

            # อัปเดตฟอร์มลูกหรือฟอร์มแม่
            if instance.parent:
                parent_form = instance.parent
                parent_form.section = instance.section
                """ parent_form.start_date = instance.start_date """
                parent_form.end_date = instance.end_date
                parent_form.description = instance.description
                parent_form.save()
            else:
                child_forms = instance.sub_items.all()
                for child in child_forms:
                    child.section = instance.section
                    """ child.start_date = instance.start_date
                    child.end_date = instance.end_date """
                    child.description = instance.description
                    child.save()

        return instance



class Assessment_Form(forms.ModelForm): #หน้าสร้างแบบฟอร์ม
    class Meta:
        model = Form
        fields = ['course', 'section', 'template']
        
        widgets = {
            'semester': forms.Select(choices=((1, '1'), (2, '2'), (3, '3'))),
            'section': forms.Select(choices=()),
            #'section': forms.Select(choices=((1, 'ตอนเรียนที่ 1'), (2, 'ตอนเรียนที่ 2'), (3, 'ตอนเรียนที่ 3'), (4, 'ตอนเรียนที่ 4'), (5, 'ตอนเรียนที่ 5'), (6, 'ตอนเรียนที่ 6'), (7, 'ตอนเรียนที่ 7'), (8, 'ตอนเรียนที่ 8'), (9, 'ตอนเรียนที่ 9'), (10, 'ตอนเรียนที่ 10'))),
            #'start_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True, 'readonly': False}),
            #'end_date': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True, 'readonly': False}),
        }
        exclude = ['template'] 
           
    def __init__(self, *args, custom_param=None, **kwargs):
        super().__init__(*args, **kwargs)
        print(custom_param)
        
        
        """ template_instance = Teamplates.objects.get(id=custom_param) """
        # ฟิคเวลาจากแม่แบบที่หัวหน้าสาขากำหนด
        """ self.fields['start_date'].initial = custom_param.start_date
        self.fields['end_date'].initial = custom_param.end_date """
        # กรองรายวิชาที่มี section ว่างเท่านั้น
        courses_with_sections = Course.objects.filter(teamplates=custom_param).distinct()
        valid_courses = []
        
        for course in courses_with_sections:
            sections = Section.objects.filter(course=course)
            for section in sections:
                if not Form.objects.filter(course=course, section=section, template=custom_param).exists():
                    valid_courses.append(course)
                    break  # มี section ว่างอยู่ใน course นี้
        
        c_choices = [('', 'เลือกรายวิชา')] + [(c.id, f'{c.class_code} | {c.name}') for c in valid_courses]
        self.fields['course'].widget = forms.Select(choices=c_choices)
        self.fields['course'].label = 'รายวิชา'
        #self.fields['start_date'].label = 'วันเวลาเริ่มต้นการประเมิน'
        #self.fields['end_date'].label = 'วันเวลาสิ้นสุดการประเมิน'
        
        self.fields['section'].queryset = Section.objects.none()

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['section'].queryset = Section.objects.filter(course_id=course_id).exclude(
                    id__in=Form.objects.filter(course_id=course_id, template=custom_param).values_list('section_id', flat=True)
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['section'].queryset = self.instance.course.sections.exclude(
                id__in=Form.objects.filter(course=self.instance.course, template=custom_param).values_list('section_id', flat=True)
            )
        
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

class DynamicLikertForm(forms.Form):  # หน้าแบบประเมิน
    def __init__(self, *args, custom_param=None, **kwargs):
        super(DynamicLikertForm, self).__init__(*args, **kwargs)
        if custom_param:
            main_counter = 0

            # ดึงคำถามหลักที่ไม่ใช่ template_select
            questions = AssessmentItem.objects.filter(form=custom_param, parent__isnull=True, template_select__isnull=True)
            for question in questions:
                main_counter += 1
                main_question_text = f"{main_counter}. {question.text}"
                # เพิ่มคำถามหลักในฟอร์มแบบไม่ต้องการคำตอบ
                self.fields[f'question_{question.id}'] = forms.CharField(
                    label=main_question_text,
                    required=False,
                    widget=forms.TextInput(attrs={
                        'disabled': 'disabled',
                        'style': 'border: none; background-color: transparent;',
                        'class': 'text-input-disabled main-question'
                    })
                )
                # ดึงคำถามย่อย
                sub_counter = 0
                sub_questions = question.sub_items.all()
                for sub_question in sub_questions:
                    sub_counter += 1
                    sub_question_text = f"{main_counter}.{sub_counter} {sub_question.text}"
                    self.fields[f'sub_question_{sub_question.id}'] = forms.ChoiceField(
                        label=sub_question_text,
                        choices=LIKERT_CHOICES,
                        widget=forms.RadioSelect(attrs={
                            'class': 'radio-select sub-question',
                            'style': 'margin-left: 20px;'  # เพิ่มระยะห่างสำหรับคำถามย่อย
                        })
                    )
            
            # ดึงคำถามหลักที่เป็น template_select
            template_questions = AssessmentItem.objects.filter(form=custom_param, parent__isnull=True, template_select__isnull=False)
            for template_question in template_questions:
                # เพิ่มคำถามหลักจาก TemplateData ในฟอร์มแบบไม่ต้องการคำตอบ
                self.fields[f'template_question_{template_question.id}'] = forms.CharField(
                    label=f"{template_question.template_select.text}",
                    required=False,
                    widget=forms.TextInput(attrs={
                        'disabled': 'disabled',
                        'style': 'border: none; background-color: transparent;',
                        'class': 'text-input-disabled main-question'
                    })
                )
                # ดึงคำถามย่อยจาก TemplateData
                sub_template_questions = AssessmentItem.objects.filter(parent=template_question)
                for sub_template_question in sub_template_questions:
                    self.fields[f'template_sub_question_{sub_template_question.id}'] = forms.ChoiceField(
                        label=f"{sub_template_question.template_select.text}",
                        choices=LIKERT_CHOICES,
                        widget=forms.RadioSelect(attrs={
                            'class': 'radio-select sub-question',
                            'style': 'margin-left: 20px;'  # เพิ่มระยะห่างสำหรับคำถามย่อย
                        })
                    )