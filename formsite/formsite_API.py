from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.http import JsonResponse
import json
from django.template.loader import get_template
from django.db.models import Avg
import pdfkit
from django.template.loader import render_to_string
import os

def set_active (request):
    if request.method == 'POST':
        id = request.POST.get('form_id')
        if id is not None:
            tem_in = Teamplates.objects.get(id=id)
            if not tem_in.is_active  :
                Teamplates.objects.filter(department=tem_in.department).update(is_active=False)
                tem_in.is_active = True
                tem_in.save()
                
            
                return JsonResponse({'status': 'success'}, status=201)
            elif tem_in.is_active:
                tem_in.is_active = False
                tem_in.save()
                return JsonResponse({'status': 'success'}, status=200)
            
        return JsonResponse({'status': 'bad request'}, status=400)
    
def manage_courses_API(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        class_code = data.get('class_code')
        name = data.get('name')
        sections_count = int(data.get('sections', 0))

        user_profile = get_object_or_404(UserProfile, user=request.user)
        template = Teamplates.objects.get(department=user_profile.department, is_active=True)
        
        course = Course.objects.create(class_code=class_code, name=name, teamplates=template)
        for i in range(1, sections_count + 1):
            print(i)
            Section.objects.create(course=course, session_number=i)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

def delete_course_API(request, id):
    if request.method == 'DELETE':
        try:
            course = Course.objects.get(id=id)
            course.delete()
            return JsonResponse({'success': True})
        except Course.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Course does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

            
def get_Templates_by_departmen(request):
    department_id = request.GET.get('department_id')
    print(department_id)
    templates = Teamplates.objects.filter(department=department_id)
    
    templates_list = list(templates.values('id', 'year_number', 'semester'))
    return JsonResponse(templates_list, safe=False)

WKHTMLTOPDF_CMD = r'D:\wkhtmltopdf\bin\wkhtmltopdf.exe'

def download_pdf(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    assessment_items = AssessmentItem.objects.filter(
        form=form, parent__isnull=True, template_select__isnull=True
    ).annotate(
        average_response=Avg('assessmentresponse__response')
    )
    
    plo = AssessmentItem.objects.filter(
        form=form, parent__isnull=True, template_select__isnull=False
    ).annotate(
        average_response=Avg('assessmentresponse__response')
    )
    
    total_sub_avg_list = []

    # สำหรับ assessment_items
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

    # โหลด HTML template
    html = render_to_string('report_pdf.html', {
        'form': form,
        'assessment_items': assessment_items,
        'plo': plo,
        'overall_plo_average': overall_plo_average
    })

    # ตั้งค่า options สำหรับ pdfkit
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'enable-local-file-access': None
    }

    # สร้าง PDF ด้วย pdfkit
    pdf = pdfkit.from_string(html, False, options=options, configuration=pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD))

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{form_id}.pdf"'

    return response

def update_course(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('id')
        class_code = data.get('class_code')
        name = data.get('name')
        
        a=course_id.split('-')

        course = get_object_or_404(Course, id=a[1])
        course.class_code = class_code
        course.name = name
        course.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)