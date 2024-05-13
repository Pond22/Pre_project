from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from formsite.models import TemplateData, AssessmentItem, Teamplates, UserProfile, AuthorizedUser
from formsite.models import Form as form_model
from .forms import PLOsForm, Assessment_Form, ClosForm, CSVUploadForm, PLOstest
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import time
# Create your views here.

def user_is_teacher(user):
    return user.groups.filter(name='อาจารย์').exists() or user.is_superuser

def teacher_required(view_func):
    decorated_view_func = user_passes_test(user_is_teacher)
    
    def wrapper(request, *args, **kwargs):
        if not user_is_teacher(request.user):
            return HttpResponse("TEACHER ONLY!")
        return view_func(request, *args, **kwargs)
    
    return wrapper

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


#@login_required(login_url="sign_in")
@teacher_required
def create_form(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    Active_Template = Teamplates.objects.get(is_active=True, department=user_profile.department)
    if request.method == 'POST':
        stu_name_list = request.POST.getlist('stu_name_list[]')
        stu_num_list = request.POST.getlist('stu_num_list[]')
        
        for round in range(2):
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
                new_in.template = Active_Template      
                if round == 1: #ถ้าเป็นครั้งที่สองสร้างของอาจารย์
                    new_in.is_teacher_form = True
                    new_in.save()
                if round == 0: #ถ้าเป็นสร้างครั้งแรก ทำแบบฟอร์มของนักเรียนแล้วเอาชื่อเข้า
                    start_time = time.time()
                    print("PASS1")
                    new_in.save()
                    if (len(stu_num_list) == len(stu_name_list)):
                        print("PASS2")
                        for index in range(len(stu_num_list)):
                            print(index)
                            name = stu_name_list[index]
                            password = stu_num_list[index]  
                            email = str(stu_num_list[index]) + '@payap.ac.th'
                            if not User.objects.filter(username=name).exists():
                                user = User.objects.create_user(username=name, email=email, password=str(password))
                                group = Group.objects.get(name='นักศึกษา')
                                user.groups.add(group)  
                                AuthorizedUser.objects.create(form=new_in, users=user)
                            else:
                                user_instance = User.objects.get(username=name)
                                AuthorizedUser.objects.create(form=new_in, users=user_instance)
                end_time = time.time()
                print("เวลาในการสร้างรายชื่อ = ",end_time - start_time)            
                create_form = get_object_or_404(form_model, id=new_in.id)
                if 'main_field0' in request.POST:  
                    for i in range(le + 1):
                        name_main = 'main_field' + str(i)
                        main_fields = request.POST.get(name_main, '') 
                        #print('main_fields =', name_main)
                        main_field = AssessmentItem.objects.create(text=main_fields, form=create_form)
                        
                        name_sub = 'sub_field_' + str(name_main)
                        sub_fields = request.POST.getlist(name_sub)
                        #print(sub_fields)
                        #print('name_sub =', name_sub)

                        for sub_field_text in sub_fields:
                            sub_field = AssessmentItem.objects.create(text=sub_field_text, parent=main_field, form=create_form)
                        
                    count = 0 #ทำขั้นตอนบันทึก PLOs
                    while True:
                        main_field_name = f'id_main_{count}'
                        sub_field_name = f'id_sub_{count}'


                        if main_field_name in request.POST:
                            main_id = request.POST[main_field_name]
                            main_template_data = TemplateData.objects.get(id=main_id)

                            template_main_field = AssessmentItem.objects.create(
                                template_select=main_template_data, form=create_form
                            )

                            sub_ids = request.POST.getlist(sub_field_name) 
                            for sub_id in sub_ids:
                                sub_template_data = TemplateData.objects.get(id=sub_id)
                                AssessmentItem.objects.create(
                                    template_select=sub_template_data, parent=template_main_field, form=create_form
                                )
                        else:
                            break

                        count += 1
        return HttpResponse("Data saved successfully!")
             
    else:
        
        """ template_data = list(Active_Template.TemplateDataset.all())
        for form in template_data:
            print(form) """
            
        template_data = []
        if Active_Template:
            template_data = Active_Template.TemplateData.all()
            
        #courses = Course.objects.filter(teamplates=Active_Template)
        new_form = Assessment_Form(custom_param=Active_Template)
      
        #new_form.set_courses_choices(courses)
  
        return render(request, 'evaluate/create_form.html', {'new_form': new_form, 'template_data':template_data})
    
    ''''
    form = Form.objects.get(id=form_id)
    items = AssessmentItem.objects.filter(form=form)  ทดสอบคิวรี่
    for item in items:
        responses = AssessmentResponse.objects.filter(assessment_item=item)
        print(f"คำถาม: {item.text}")
        for response in responses:
            print(f"ตอบโดย: {response.respondent.username}, คำตอบ: {response.response}, ความเห็น: {response.response_comment}")'''

    
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
    clo_form = AssessmentItem.objects.filter(form=form_id, parent__isnull=True, template_select__isnull=True)
    #assessment_template_item = AssessmentItem.objects.filter(form=form_id, template_select__isnull=False)
    assessment_template_item = AssessmentItem.objects.filter(form=form_id)
    csv_1 = CSVUploadForm()
    context = {'form_instance': form_instance, 'clo_form': clo_form, 'csv_1': csv_1, 'assessment_template_item': assessment_template_item}
    return render(request, 'evaluate/main_form.html', context)

def handle_csv_upload(request, form_id):
    form = CSVUploadForm(request.POST, request.FILES)
    use_aut = Aut(request.POST)
    if not form.is_valid():
        return False

    id_form = get_object_or_404(form_model, id=form_id)
    existing_user = id_form.users.all
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
        if not existing_user:
            id_form.users.add(row[0])

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