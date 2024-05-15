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

def view_form(request):
    if request.method == 'POST':
        #form = RegisterForm(request.POST)
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            start_time = time.time()
            csv_file = request.FILES['csv_file']
            id_form = get_object_or_404(form_id, id=4)
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
                        user.groups.add(group) 
                    except :
                        None
                    #AuthorizedUser.objects.create(form = id_form, stu_list=row[0])
                    processed_records +=1
        end_time = time.time()
        execution_time = end_time - start_time
        write_to_file(execution_time, 'DJANGO_VIEWS')
    
    csv_1 = CSVUploadForm()
    context = {'csv_1': csv_1}
    return render(request, 'test.html', context)
    
'''
def view_form(request):
    csv_1 = CSVUploadForm()
    context = {'csv_1': csv_1}
    return render(request, 'test.html', context)
    
class CSV_API(viewsets.ViewSet):
    serializer_class = CSV_API
    def create(self, request):
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            return Response({'error': 'No CSV file provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'Invalid file format. Please provide a CSV file'}, status=status.HTTP_400_BAD_REQUEST)

        id_form = get_object_or_404(form_id, id=4)
        start_time = time.time()
        if csv_file.name.endswith('.csv'):
                print("START")
                start_time = time.time()
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
                        #print("ซ้ำ",index )
                        None
                    AuthorizedUser.objects.create(form = id_form, stu_list=row[0])
                    processed_records +=1
                    sum = (processed_records/num_rows)*100
        end_time = time.time()
        execution_time = end_time - start_time
        write_to_file(execution_time, 'API_UPLOAD')
        #print("Execution time:", execution_time, "seconds")
        return Response({'sum': sum}, status=status.HTTP_201_CREATED)
    
'''

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
    
def manage_template(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    template = Teamplates.objects.filter(department=user_profile.department)
    
    if request.method == "POST":
        pass
    else:
        template = Teamplates.objects.filter(department=user_profile.department)
        for data in template:
            for template_data in data.TemplateData.all():
                print(template_data.text)
            # แสดงข้อมูลจากโมเดล CLO ที่เชื่อมโยงกับ Teamplates นี้
            """ for clo in data.CLO.all():
                print(clo.text) """
    return render(request, 'manage_template.html', {'form': template, 'user_profile': user_profile})

def edit_template(request, form_id):

    template = Teamplates.objects.filter(id=form_id)

    return render(request, 'edit_template.html', {'template': template})

#อัพเดตข้อมูล PLO&O ใน Temlplate ที่มีอยู่ก่อน ลบด้วย
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
