from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from formsite.models import PLOs, clo, AuthorizedUser
from formsite.models import form as form_model
from .forms import PLOsForm, Form, ClosForm, CSVUploadForm, Aut, PLOstest
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
# Create your views here.

@login_required(login_url="sign_in")   
def eva_home(request):
    x = PLOs.objects.all().order_by("id")
    return render(request, 'evaluate/evaluate_home.html', {'plo':x})
    
@login_required(login_url="sign_in")   
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


@login_required(login_url="sign_in")
def create_form(request):
    if request.method == 'POST':
        new_form = Form(request.POST)
        if new_form.is_valid():
            new_in = new_form.save(commit=False)
            new_in.created_by = request.user
            new_in.save()
            return redirect('create_clo', new_in.id) 
    else:
        new_form = Form()
        return render(request, 'evaluate/create_form.html', {'new_form': new_form})
    
@login_required(login_url="sign_in")  
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

@login_required(login_url="sign_in")    
def form_detail(request):
    user = request.user
    forms = form_model.objects.filter(created_by=user)
    context = {'forms': forms}
    return render(request, 'evaluate/form_detail.html', context)

def progress_api(num1, num2):
    # เรียกใช้ฟังก์ชัน test เพื่อคำนวณ progress_percent
    progress_percent = (num1 / num2) * 100

    # ส่งค่า progress_percent กลับไปในรูปแบบ JSON
    return JsonResponse({'progress_percent': progress_percent})

@login_required(login_url="sign_in")   
def view_form(request, form_id):
    y = get_object_or_404(form_model, id=form_id)
    if request.user.username != str(y.created_by) :
        return redirect('http://127.0.0.1:8000/form/form_detail')
    if request.method == 'POST':
        #form = RegisterForm(request.POST)
        form = CSVUploadForm(request.POST, request.FILES)
        use_aut = Aut(request.POST)
        id_form = get_object_or_404(form_model, id=form_id)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if csv_file.name.endswith('.csv'):
                #csv_data = csv_file.read().decode('utf-8')
                try:
                    csv_data = pd.read_csv(csv_file, encoding='utf-8')
                except UnicodeDecodeError:
                    csv_data = pd.read_csv(csv_file, encoding='latin1')
                #csv_data = StringIO(csv_data)
                #reader = csv.reader(csv_data)
                num_rows = len(csv_data)
                processed_records =0
                for index, row in csv_data.iterrows():
                    try:
                        name = row[1]
                        password = row[0]  # ใช้คอลัมน์ที่ 0 เป็นรหัสผ่าน
                        email = str(row[0]) + '@payap.ac.th'
                        user = User.objects.create_user(username=name, email=email, password=str(password))
                        group = Group.objects.get(name='นักศึกษา')
                        user.groups.add(group)  # เพิ่มเข้ากลุ่มที่ 2
                    except :
                        print("ซ้ำ")
                    AuthorizedUser.objects.create(form=id_form, stu_list=row[0])
                    progress_api(processed_records, num_rows)
                    processed_records +=1
                
    form_instance = get_object_or_404(form_model, pk=form_id)
    clo_form = clo.objects.filter(form=form_id)
    print("form_id = ",form_id)
    csv_1 = CSVUploadForm()
    context = {'form_instance': form_instance, 'clo_form': clo_form, 'csv_1': csv_1}
    return render(request, 'evaluate/main_form.html', context)

def dy (request):
    if request.method == 'POST':
        length = request.POST.get('length')
        if length is None:
            length = 1
        length = int(length)
        new_PLOstest = PLOstest(request.POST)
        if new_PLOstest.is_valid():
            for i in range(length):
                str1 = "text_"+ str(i+1)
                if request.POST.get(str1):
                    text = request.POST.get(str1)
                    print(text)
                    user1 = request.user
                    PLOs.objects.create(created_by=user1, text=text)
                else:
                    print("NULL")
    return render(request, 'evaluate/Dynamic_Form.html', {'form':PLOstest})
