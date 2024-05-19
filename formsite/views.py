from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from .models import *
from .models import Form as form_id
import time
import pandas as pd
from .forms import Plo_form
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
            plo_form_instance.save()
        if le is None:
            le = 0
        else:
            le = int(le)
        
        print(le)
        print('ไอดี = ',plo_form_instance.id)
        print('year = '+year)
        create_form = get_object_or_404(Teamplates, id=plo_form_instance.id)
        if 'main_field0' in request.POST:  
            for i in range(le + 1):
                name_main = 'main_field' + str(i)
                print(name_main,i)
                if (i ==0): # ถ้าเป็น 0 บันทุก O
                    main_fields = request.POST.get(name_main, '') 
                    main_field = CLO.objects.create(text=main_fields, form=create_form)
                        
                    name_sub = 'sub_field_' + str(name_main)
                    sub_fields = request.POST.getlist(name_sub)

                    for sub_field_text in sub_fields:
                        CLO.objects.create(text=sub_field_text, parent=main_field, form=create_form)
                       
                else:        
                 #  นอกเหนือจาก 0 บันทีกลง PLO   
                    main_fields = request.POST.get(name_main, '') 
                    main_field = TemplateData.objects.create(text=main_fields, form=create_form)
                            
                    name_sub = 'sub_field_' + str(name_main)
                    sub_fields = request.POST.getlist(name_sub)

                    for sub_field_text in sub_fields:
                        TemplateData.objects.create(text=sub_field_text, parent=main_field, form=create_form)

        return HttpResponse("Data saved successfully!")
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
    
    if  not tem.department == user_profile.department:
        return redirect('/manage_template')
        

    return render(request, 'edit_template.html', {'template': template})

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
    
    elif request.method == 'DELETE' :
        data_id = request.GET.get('data_id')
        data_type = request.GET.get('type')  
      
        if data_type == 'TemplateData':
            TemplateData.objects.filter(id=data_id).delete()
            print("delete",data_id)
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
    
            TemplateData.objects.create(form = template_in, text ="")
            return JsonResponse({'status': 'success', 'message': 'Data updated successfully'})
        
        elif request.POST.get('type') != "Newparent":
            parent_id = request.POST.get('data_id').split('_')[2] 
            text = request.POST.get('text')
            print(request.POST.get('text'))
            data_type = request.POST.get('type')
            if text is not None and text.strip() != "" :
                tempalte_in = Teamplates.objects.get(id=request.POST.get('form_id'))
                if data_type == 'TemplateData':
                    # สร้างหรืออัพเดต TemplateData ใหม่
                    TemplateData.objects.update_or_create(parent=TemplateData.objects.get(id=parent_id), text=text, form = tempalte_in)
                elif data_type == 'CLO':
                    # สร้างหรืออัพเดต CLO ใหม่
                    CLO.objects.update_or_create(parent=CLO.objects.get(id=parent_id), text=text, form =tempalte_in)
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
@committee_required
@teacher_required
def report_main(request):
    forms = Form.objects.filter(expired=True)

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
@committee_required
@teacher_required
def report(request, form_id):
    
    form = get_object_or_404(Form, id=form_id)
    assessment_items = AssessmentItem.objects.filter(form=form, parent__isnull=True,template_select__isnull=True).annotate(average_response=Avg('assessmentresponse__response'))
    plo = AssessmentItem.objects.filter(form=form, parent__isnull=True,template_select__isnull=False).annotate(average_response=Avg('assessmentresponse__response'))
    comment = CommentForm.objects.filter(form=form,comment__isnull=False)

    if form.created_by != request.user and not request.user.groups.filter(name='กรรมการ').exists():
        return redirect('/report_main')

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
    
    return render(request, 'report.html', {'form':form, 'assessment_items': assessment_items, 'plo':plo, 'overall_plo_average':overall_plo_average, 'comment':comment})
    
'''
def edit_template(request):
    if request.method == 'POST':
        #แก้ไข
        if 'main_text' in request.POST and 'plo_id' in request.POST:
            
            plo_id = request.POST.get('plo_id')
            new_text = request.POST.get('main_text')
            try:
                plo = get_object_or_404(TemplateData, id=plo_id)
                plo.text = new_text
                plo.save()
                return redirect('manage_plos')
            except TemplateData.DoesNotExist:
                return HttpResponse("PLO does not exist.")
        elif 'sub_text' in request.POST and 'sub_item_id' in request.POST:
            
            sub_item_id = request.POST.get('sub_item_id')
            sub_text = request.POST.get('sub_text')
            try:
                sub_plo = get_object_or_404(TemplateData, id=sub_item_id)
                sub_plo.text = sub_text
                sub_plo.save()
                return redirect('manage_plos')
            except TemplateData.DoesNotExist:
                return HttpResponse("Sub PLO does not exist.")
        else:
            return HttpResponse("Invalid form data.")
        #แก้ไข
    
    elif request.method == 'GET':
        year_number = request.GET.get('year_number')
        school_year = request.GET.get('school_year')
        plos_form = Teamplates.objects.filter(created_by=request.user)
        return render(request, 'manage_plos.html', {'plos': plos_form})
    else:
        plos_form = TemplateData.objects.filter(parent__isnull=True)
        return render(request, 'manage_plos.html', {'plos': plos_form})
'''
