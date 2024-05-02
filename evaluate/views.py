from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from formsite.models import TemplateData, AssessmentItem, AuthorizedUser, Teamplates
from formsite.models import Form as form_model
from .forms import PLOsForm, Assessment_Form, ClosForm, CSVUploadForm, Aut, PLOstest
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
# Create your views here.

@login_required(login_url="sign_in")   
def eva_home(request):
    x = TemplateData.objects.all().order_by("id")
    return render(request, 'evaluate/evaluate_home.html', {'plo':x})
    
@login_required(login_url="sign_in")   #Not used here
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
        le = request.POST.get('length')
        if le is None:
            le = 0
        else:
            le = int(le)
        print(le)

        new_form = Assessment_Form(request.POST)
        if new_form.is_valid():
            new_in = new_form.save(commit=False)
            new_in.created_by = request.user
            new_in.save()
            
            #somthing = 'main_field0'
            
            if 'main_field0' in request.POST:  
                for i in range(le + 1):
                    create_form = get_object_or_404(form_model, id=new_in.id)
                    name_main = 'main_field' + str(i)
                    main_fields = request.POST.get(name_main)  # ใช้ค่าว่างในกรณีที่ไม่พบค่า
                    print('main_fields =', name_main)
                    main_field = AssessmentItem.objects.create(text=main_fields, form=create_form)
                    
                    name_sub = 'sub_field_' + str(name_main)
                    sub_fields = request.POST.getlist(name_sub)
                    print(sub_fields)
                    print('name_sub =', name_sub)

                    for sub_field_text in sub_fields:
                        sub_field = AssessmentItem.objects.create(text=sub_field_text, parent=main_field)

                return HttpResponse("Data saved successfully!")
            else:
                return HttpResponse("Error: No data for 'main_field0'")  
    else:
        active_forms = Teamplates.objects.filter(is_active=True).prefetch_related('templatedata_set')
        template_data = {}

        for form in active_forms:
            template_data[form] = list(form.templatedata_set.all())
                    
        print(template_data)
        new_form = Assessment_Form()
        user_now = request.user.username
        return render(request, 'evaluate/create_form.html', {'new_form': new_form, 'template_data': template_data, 'user_now':user_now})

    
@login_required(login_url="sign_in")  
def create_clo(request, form_id): #Not use here
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
    context = {'forms': forms, 'user':user}
    return render(request, 'evaluate/form_detail.html', context)


@login_required(login_url="sign_in")   
def view_form(request, form_id):
    name_who_created = get_object_or_404(form_model, id=form_id)
    if request.user.username != str(name_who_created.created_by):
        return redirect('http://127.0.0.1:8000/form/form_detail')

    if request.method == 'POST':
        if handle_csv_upload(request, form_id):
            print("handle_csv_upload")
        elif handle_clo_update(request):
            print("handle_clo_update")
        elif handle_sub_clo_update(request):
            print("handle_sub_clo_update")
        elif handle_clo_delete(request):
            print("handle_clo_delete")
        elif handle_sub_clo_delete(request):
            print("handle_sub_clo_delete")
            
        else:
            return HttpResponse("Invalid form data.")
    
    form_instance = get_object_or_404(form_model, pk=form_id)
    clo_form = AssessmentItem.objects.filter(form=form_id, parent__isnull=True)
    csv_1 = CSVUploadForm()
    context = {'form_instance': form_instance, 'clo_form': clo_form, 'csv_1': csv_1}
    return render(request, 'evaluate/main_form.html', context)

def handle_csv_upload(request, form_id):
    form = CSVUploadForm(request.POST, request.FILES)
    use_aut = Aut(request.POST)
    if not form.is_valid():
        return False

    id_form = get_object_or_404(form_model, id=form_id)
    csv_file = request.FILES['csv_file']
    if not csv_file.name.endswith('.csv'):
        return False

    try:
        csv_data = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        csv_data = pd.read_csv(csv_file, encoding='latin1')
    num_rows = len(csv_data)

    for index, row in csv_data.iterrows():
        try:
            name = row[1]
            password = row[0]  # ใช้คอลัมน์ที่ 0 เป็นรหัสผ่าน
            email = str(row[0]) + '@payap.ac.th'
            user = User.objects.create_user(username=name, email=email, password=str(password))
            group = Group.objects.get(name='นักศึกษา')
            user.groups.add(group)  # เพิ่มเข้ากลุ่มที่ 2
        except Exception as e:
            print("Error:", e)
            print("ซ้ำ")
        AuthorizedUser.objects.create(form=id_form, stu_list=row[0])

    return True

def handle_clo_update(request):
    if 'main_text' not in request.POST or 'clo_id' not in request.POST:
        return False
    
    clo_id = request.POST.get('clo_id')
    new_text = request.POST.get('main_text')
    try:
        plo = get_object_or_404(AssessmentItem, id=clo_id)
        plo.text = new_text
        plo.save()
        return True
    except TemplateData.DoesNotExist:
        return False

def handle_sub_clo_update(request):
    if 'sub_text' not in request.POST or 'sub_item_id' not in request.POST:
        return False
    
    sub_item_id = request.POST.get('sub_item_id')
    sub_text = request.POST.get('sub_text')
    try:
        sub_plo = get_object_or_404(AssessmentItem, id=sub_item_id)
        sub_plo.text = sub_text
        sub_plo.save()
        return True
    except TemplateData.DoesNotExist:
        return False

def handle_clo_delete(request):
    if 'clo_id' not in request.POST:
        return False
    
    clo_id = request.POST.get('clo_id')
    try:
        clo_obj = get_object_or_404(AssessmentItem, id=clo_id)
        clo_obj.delete()
        return True
    except AssessmentItem.DoesNotExist:
        return False

def handle_sub_clo_delete(request):
    if 'sub_item_id' not in request.POST:
        return False
    
    sub_item_id = request.POST.get('sub_item_id')
    try:
        sub_clo_obj = get_object_or_404(AssessmentItem, id=sub_item_id)
        sub_clo_obj.delete()
        return True
    except AssessmentItem.DoesNotExist:
        return False

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
                    TemplateData.objects.create(created_by=user1, text=text)
                else:
                    print("NULL")
    return render(request, 'evaluate/Dynamic_Form.html', {'form':PLOstest})






#สำหรับการบันทึก 2 รอบรอบแรกจะเป็น form สำหรับนักศึกษาที่มีสิทธ์ประเมินรายวิชานั้นๆ รอบที่ 2 จะบันทึกสำหรับอาจารย์
'''
@login_required(login_url="sign_in")
def create_form(request):
    if request.method == 'POST':
        for i in range(2):
            
            le = request.POST.get('length')
            if le is None:
                le = 0
            else:
                le = int(le)

            new_form = Form(request.POST)
            if new_form.is_valid():
                new_in = new_form.save(commit=False)
                new_in.created_by = request.user
                if i==1 :
                    new_in.Active = True
                new_in.save()
                
                #somthing = 'main_field0'
                
                if 'main_field0' in request.POST:
                    for i in range(le + 1):
                        create_form = get_object_or_404(form_model, id=new_in.id)
                        name_main = 'main_field' + str(i)
                        main_fields = request.POST.get(name_main)  # ใช้ค่าว่างในกรณีที่ไม่พบค่า
                        print('main_fields =', name_main)
                        main_field = AssessmentItem.objects.create(text=main_fields, form=create_form, created_by=request.user)
                        
                        name_sub = 'sub_field_' + str(name_main)
                        sub_fields = request.POST.getlist(name_sub)
                        print(sub_fields)
                        print('name_sub =', name_sub)

                        for sub_field_text in sub_fields:
                            sub_field = AssessmentItem.objects.create(text=sub_field_text, parent=main_field, form=create_form, created_by=request.user)

                    return HttpResponse("Data saved successfully!")
                else:
                    return HttpResponse("Error: No data for 'main_field0'")  
    else:
        new_form = Form()
        return render(request, 'evaluate/create_form.html', {'new_form': new_form})
        '''