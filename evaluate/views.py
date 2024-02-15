from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from formsite.models import PLOs
from .forms import PLOsForm
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
