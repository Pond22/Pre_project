from django.shortcuts import render
from django.http.response import HttpResponse
from .models import *
from .forms import Form

# Create your views here.

#def index(request):
    #return render(request, '/index.html')
    
def home(request):
    #x = form.objects.filter(id__range=(1,4), name__in=("วิชาภาษาไทย", "วิชาภาษาซี"))
    x  = form.objects.filter(class_code__in=("se211", "SE5555"))
    return render(request, 'home.html', {'data': x})

def index(request):
    return render(request, 'index.html')

