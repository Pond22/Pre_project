from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.http import JsonResponse
import json

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
            