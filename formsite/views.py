from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from .models import *
from .models import Form as form_id
import time
import pandas as pd
from .forms import Plo_form, UpdateTemplateForm
from evaluate.forms import PLOsForm, Form, ClosForm, CSVUploadForm
from django.contrib.auth.models import User, Group
from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response
from .serializers import CSVUploadForm as CSV_API
from .models import TemplateData, Teamplates
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib.auth.decorators import login_required, user_passes_test
from formsite.user_detect import*
# Create your views here.

#def index(request):
    #return render(request, '/index.html')


def home(request):
    #x = form.objects.filter(id__range=(1,4), name__in=("วิชาภาษาไทย", "วิชาภาษาซี"))
    x  = Form.objects.filter(class_code__in=("se211", "SE5555"))
    return render(request, 'home.html', {'data': x})

def index(request):
    return render(request, 'index.html')

def write_to_file(time, name):
    name = str(name)+'.txt'
    file_path = r'E:\Django_logs/'+name

    with open(file_path, 'a') as file:
        file.write("เวลา : "+str(time) + "\n")

    return print("END")

@login_required(login_url="sign_in")
@admin_required 
def create_plo(request):
    user_profile = get_object_or_404(UserProfile, user=request.user) #คิวรี่แอดมินที่เข้าหน้านั้นตอนนั้นมาหาสาขา
    
    if request.method == "POST":
        school = request.POST.get('school_year')
        year = request.POST.get('year_number')
        le = request.POST.get('length')
        
        form = Plo_form(request.POST)
        if form.is_valid():
            plo_form_instance = form.save(commit=False)
            plo_form_instance.created_by = request.user
            plo_form_instance.department = user_profile.department
            
            try:
                plo_form_instance.full_clean()  # ตรวจสอบความถูกต้อง
                plo_form_instance.save()
            except ValidationError as e:
                # เพิ่มข้อผิดพลาดในฟอร์ม
                form.add_error(None, "ปีและเทอมนี้ซ้ำกัน")
                return render(request, 'create_plos.html', {'form': form, 'user_profile': user_profile})
        else:
            # ถ้าฟอร์มไม่ valid
            return render(request, 'create_plos.html', {'form': form, 'user_profile': user_profile})
            
            
        if le is None:
            le = 0
        else:
            le = int(le)
        
        print(le)
        print('ไอดี = ',plo_form_instance.id)
        print('year = '+year)
        """ print(request.POST) """
        create_form = get_object_or_404(Teamplates, id=plo_form_instance.id)
        if 'static_field0' in request.POST:  
            for i in range(le + 1):
                name_main = 'main_field' + str(i)
                print(name_main,i)
                
                if (i ==0): # ถ้าเป็น 0 บันทุก O
                     for j in range(4):
                        name_static = 'static_field' + str(j)
                        static_fields = request.POST.get(name_static)
                        static_field = CLO.objects.create(text=static_fields, form=create_form)
                            
                        static_sub = 'sub_field_static_field' + str(j)
                        sub_fields = request.POST.getlist(static_sub)
                        print('ชื่อฟิลด์ลูก static', static_sub)
                        print(sub_fields)
                        """ print(request.POST) """

                        for sub_field_text in sub_fields:
                            CLO.objects.create(text=sub_field_text, parent=static_field, form=create_form)
                       
                else:        
                 #  นอกเหนือจาก 0 บันทีกลง PLO   
                    main_fields = request.POST.get(name_main, '') 
                    if main_fields:
                         main_fields = f'PLO{i}: ' + main_fields
                    main_field = TemplateData.objects.create(text=main_fields, form=create_form)
    
                            
                    name_sub = 'sub_field_' + str(name_main)
                    sub_fields = request.POST.getlist(name_sub)
                    
                    sub_count = 1
                    for sub_field_text in sub_fields:
                        if sub_field_text:
                            data = f'{i}.{sub_count} ' + sub_field_text
                        TemplateData.objects.create(text=data, parent=main_field, form=create_form)
                        sub_count+=1

        return redirect('/manage_template')
    else:
        form = Plo_form
        #print(user_profile.department)
        return render(request, 'create_plos.html', {'form': form, 'user_profile':user_profile})
    
@login_required(login_url="sign_in")
@admin_required      
def manage_template(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    template = Teamplates.objects.filter(department=user_profile.department)
    
    if request.method == "POST":
        pass
    else:
        template = Teamplates.objects.filter(department=user_profile.department).order_by('-is_active') 
        """ for data in template:
            for template_data in data.TemplateData.all():
                print(template_data.text)
            # แสดงข้อมูลจากโมเดล CLO ที่เชื่อมโยงกับ Teamplates นี้
            for clo in data.CLO.all():
                print(clo.text) """
    return render(request, 'manage_template.html', {'form': template, 'user_profile': user_profile})

@login_required(login_url="sign_in") 
def edit_template(request, form_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    template = Teamplates.objects.filter(id=form_id)
    tem = get_object_or_404(Teamplates, id=form_id)
    
    if not tem.department == user_profile.department:
        return redirect('/manage_template')
    
    update = UpdateTemplateForm(instance=tem, start_date=tem.start_date, end_date=tem.end_date)
    return render(request, 'edit_template.html', {'template': template, 'update':update})

#อัพเดตข้อมูล PLO&O ใน Temlplate ที่มีอยู่ก่อน ลบ
def delete_update_template_data(request):
    if request.method == 'POST':
        data_id = request.POST.get('data_id')
        text = request.POST.get('text')
        data_type = request.POST.get('type')  

        if data_type == 'TemplateData':
            TemplateData.objects.filter(id=data_id).update(text=text)
        elif data_type == 'CLO':
            CLO.objects.filter(id=data_id).update(text=text)
        return JsonResponse({'status': 'success', 'message': 'Data updated successfully'})
    
    elif request.method == 'DELETE':
        data_id = request.GET.get('data_id')
        data_type = request.GET.get('type')  
      
        if data_type == 'TemplateData':
            parent_template = TemplateData.objects.get(id=data_id).parent
            TemplateData.objects.filter(id=data_id).delete()
            print("delete", data_id)
            
            # Update the sequence of the children
            if parent_template:
                children = TemplateData.objects.filter(parent=parent_template).order_by('id')
                for index, child in enumerate(children, start=1):
                    parent_number = ''.join(filter(str.isdigit, parent_template.text.split(' ')[0]))
                    child.text = f'{parent_number}.{index} ' + ' '.join(child.text.split(' ')[1:])
                    child.save()

        elif data_type == 'CLO':
            CLO.objects.filter(id=data_id).delete()

        return JsonResponse({'status': 'success', 'message': 'Delete successfully'})
    
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

#เพิ่มข้อมูล PLO&O ใน Temlplate ที่มีอยู่ก่อน
def addnew_template_data(request):
    if request.method == 'POST':
        if request.POST.get('type') == "Newparent":
            template_in = get_object_or_404(Teamplates, id=request.POST.get('form_id'))

            # ตรวจสอบจำนวน TemplateData ที่มีอยู่แล้วใน form
            count = TemplateData.objects.filter(form=template_in, parent__isnull=True).count()
            main_fields = f'PLO{count + 1}: '

            TemplateData.objects.create(form=template_in, text=main_fields)
            return JsonResponse({'status': 'success', 'message': 'Data updated successfully'})

        elif request.POST.get('type') != "Newparent":
            parent_id = request.POST.get('data_id').split('_')[2]
            text = request.POST.get('text')
            print(request.POST.get('text'))
            data_type = request.POST.get('type')
            if text is not None and text.strip() != "":
                template_in = Teamplates.objects.get(id=request.POST.get('form_id'))

                if data_type == 'TemplateData':
                    parent_template = TemplateData.objects.get(id=parent_id)
                    # ตรวจสอบจำนวนลูกที่มีอยู่แล้วของแม่
                    sub_count = TemplateData.objects.filter(parent=parent_template).count() + 1
                    # ดึงเฉพาะตัวเลขจากข้อความของแม่
                    parent_number = ''.join(filter(str.isdigit, parent_template.text.split(' ')[0]))
                    data = f'{parent_number}.{sub_count} ' + text

                    # สร้างหรืออัพเดต TemplateData ใหม่
                    TemplateData.objects.update_or_create(
                        parent=parent_template, text=data, form=template_in)
                elif data_type == 'CLO':
                    parent_clo = CLO.objects.get(id=parent_id)
                    # ตรวจสอบจำนวนลูกที่มีอยู่แล้วของแม่
                    sub_count = CLO.objects.filter(parent=parent_clo).count() + 1
                    # ดึงเฉพาะตัวเลขจากข้อความของแม่
                    parent_number = ''.join(filter(str.isdigit, parent_clo.text.split(' ')[0]))
                    data = f'{parent_number}.{sub_count} ' + text

                    # สร้างหรืออัพเดต CLO ใหม่
                    CLO.objects.update_or_create(
                        parent=parent_clo, text=data, form=template_in)
                return JsonResponse({'status': 'success', 'message': 'Data updated successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


    
@login_required(login_url="sign_in") 
@admin_required    
def manage_course(request):

    user_profile = get_object_or_404(UserProfile, user=request.user)
    templates = Teamplates.objects.get(department=user_profile.department, is_active=True)
    courses = Course.objects.filter(teamplates=templates)
    
    for course in courses:
        for section in course.sections.all():
            print(section.session_number) 
    
    return render(request, 'manage_course.html', {'courses':courses, 'templates':templates})

@login_required(login_url="sign_in") 
@committee_or_teacher_required
def report_main(request):
    user = request.user

    if user.groups.filter(name='กรรมการ').exists():
        # กรรมการเห็นข้อมูลทั้งหมด
        forms = Form.objects.filter(expired=True)
    else:
        # ผู้สร้างแบบฟอร์มเห็นเฉพาะข้อมูลฟอร์มที่ตนเองสร้าง
        forms = Form.objects.filter(created_by=user, expired=True)
    
    department = request.GET.get('department')
    template = request.GET.get('template')
    
    if department:
        forms = Form.objects.filter(template__department=department, expired=True)

    if template:
        forms = Form.objects.filter(template=template, expired=True)

    departments = Departments.objects.all().distinct()
    
    """ courses = Course.objects.values_list('name', flat=True).distinct() """
    
    return render(request, 'report_main.html', {'form':forms, 'departments': departments})

@login_required(login_url="sign_in") 
@committee_or_teacher_required
def report(request, form_id):
    
    form = get_object_or_404(Form, id=form_id)
    """ assessment_items = AssessmentItem.objects.filter(form=form, parent__isnull=True,template_select__isnull=True).annotate(average_response=Avg('assessmentresponse__response'))
    plo = AssessmentItem.objects.filter(form=form, parent__isnull=True,template_select__isnull=False).annotate(average_response=Avg('assessmentresponse__response'))
    comment = CommentForm.objects.filter(form=form,comment__isnull=False) """
    if form.created_by != request.user and not request.user.groups.filter(name='กรรมการ').exists():
        return redirect('/manage_member')

    if request.user.groups.filter(name='กรรมการ').exists():
        # กรรมการเห็นข้อมูลทั้งหมด
        assessment_items = AssessmentItem.objects.filter(form=form, parent__isnull=True, template_select__isnull=True).annotate(average_response=Avg('assessmentresponse__response'))
        plo = AssessmentItem.objects.filter(form=form, parent__isnull=True,template_select__isnull=False).annotate(average_response=Avg('assessmentresponse__response'))
        comment = CommentForm.objects.filter(form=form, comment__isnull=False)
    else:
         # ผู้สร้างแบบฟอร์มเห็นเฉพาะข้อมูลฟอร์มที่ตนเองสร้าง
        assessment_items = AssessmentItem.objects.filter(form=form, parent__isnull=True, template_select__isnull=True, form__created_by=request.user).annotate(average_response=Avg('assessmentresponse__response'))
        plo = AssessmentItem.objects.filter(form=form, parent__isnull=True, template_select__isnull=False, form__created_by=request.user).annotate(average_response=Avg('assessmentresponse__response'))
        comment = CommentForm.objects.filter(form=form, comment__isnull=False, form__created_by=request.user)


    user_eva = AuthorizedUser.objects.filter(form=form, done=True)
    user_all = AuthorizedUser.objects.filter(form=form)
    if len(user_all) > 0:  
        sum_user= (len(user_eva) / len(user_all)) * 100
    else:
        sum_user= 0  
    context_user = {'user_eva':user_eva, 'user_all':user_all,'sum_user':sum_user}
    
    print(sum_user)
    # สำหรับแต่ละ assessment item, กรอง sub_items และคำนวณค่าเฉลี่ย
    for item in assessment_items:
        sub_items_with_avg = item.sub_items.annotate(
            average_response=Avg('assessmentresponse__response')
        )
        item.sub_items_with_avg = sub_items_with_avg
        
         # คำนวณค่าเฉลี่ยรวมของหัวข้อใหญ่
        sub_avg_list = [sub.average_response for sub in sub_items_with_avg if sub.average_response is not None]
        if sub_avg_list:
            item.overall_average = sum(sub_avg_list) / len(sub_avg_list)
        else:
            item.overall_average = None
            
    total_sub_avg_list = []   
         
    # สำหรับ plo
    for item in plo:
        sub_items_with_avg = item.sub_items.annotate(
            average_response=Avg('assessmentresponse__response')
        )
        item.sub_items_with_avg = sub_items_with_avg
        
        # คำนวณค่าเฉลี่ยรวมของหัวข้อใหญ่
        sub_avg_list = [sub.average_response for sub in sub_items_with_avg if sub.average_response is not None]
        total_sub_avg_list.extend(sub_avg_list)  # รวมค่าเฉลี่ยของ sub_items ทั้งหมดใน total_sub_avg_list
        if sub_avg_list:
            item.overall_average = sum(sub_avg_list) / len(sub_avg_list)
        else:
            item.overall_average = None

    # คำนวณค่าเฉลี่ยรวมของทุก PLO
    if total_sub_avg_list:
        overall_plo_average = sum(total_sub_avg_list) / len(total_sub_avg_list)
    else:
        overall_plo_average = None
    
    return render(request, 'report.html', {'form':form, 'assessment_items': assessment_items, 'plo':plo, 'overall_plo_average':overall_plo_average, 'comment':comment, 'context_user':context_user})
    