from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from formsite.models import PLOs
from formsite.models import form as form_model
from .forms import PLOsForm, Form, ClosForm
from django.core.exceptions import ValidationError
# Create your views here.

@login_required(login_url="/member/sign_in")
def eva_home(request):
    x = PLOs.objects.all().order_by("id")
    return render(request, 'evaluate/evaluate_home.html', {'plo':x})
    
@login_required(login_url="/member/sign_in")
def create_plo(request):
    if request.method == "POST":
        form = PLOsForm(request.POST)  # สร้าง ModelForm จากข้อมูลที่ผู้ใช้ส่งมา
        if form.is_valid():
           
            plo_instance = form.save(commit=False)
            plo_instance.created_by = request.user
            plo_instance.save()
        return redirect('eva_home')  # ให้ redirect ไปที่หน้าหลักหลังจากบันทึกสำเร็จ
    else:
        form = PLOsForm()  # สร้างฟอร์มใหม่สำหรับการกรอกข้อมูล
        
    context = {'form': form}
    return render(request, 'evaluate/create_plo.html', context)


@login_required(login_url="/member/sign_in")
def create_form(request):
    if request.method == 'POST':
        new_form = Form(request.POST)
        if new_form.is_valid():
            new_in = new_form.save(commit=False)
            new_in.created_by = request.user
            new_in.save()
            return redirect('create_clo', new_in.id) 
    else:
        return render(request, 'evaluate/create_form.html')
    
@login_required(login_url="/member/sign_in")
def create_clo(request, form_id):
    create_form = get_object_or_404(form_model, id=form_id)
    if request.method == "POST":
        form = ClosForm(request.POST)
        if form.is_valid():
            clo_instance = form.save(commit=False)
            print("testr")
            clo_instance.text = request.POST['text']
            print(clo_instance.text)
            clo_instance.created_by = request.user
            clo_instance.form = create_form
            clo_instance.save()
            return redirect('eva_home')
        else : print ("Error creating")
    else:
        form = ClosForm()
    context = {'form': form, 'form_id': form_id}
    return render(request, 'evaluate/create_clo.html', {'context': context})

@login_required(login_url="/member/sign_in")    
def form_detail(request):
    user = request.user
    form_instance = form_model.objects.filter(created_by=user)
    return render(request, 'evaluate/form_detail.html', {'form_instance': form_instance})



