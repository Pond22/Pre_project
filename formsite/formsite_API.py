from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.http import JsonResponse

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
            