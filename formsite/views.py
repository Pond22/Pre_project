from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from .models import *
from .models import form as form_id
import time
import pandas as pd
from evaluate.forms import PLOsForm, Form, ClosForm, CSVUploadForm, Aut
from django.contrib.auth.models import User, Group
from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response
from .serializers import CSVUploadForm as CSV_API
from .models import PLOs
# Create your views here.

#def index(request):
    #return render(request, '/index.html')

def home(request):
    #x = form.objects.filter(id__range=(1,4), name__in=("วิชาภาษาไทย", "วิชาภาษาซี"))
    x  = form.objects.filter(class_code__in=("se211", "SE5555"))
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
                    AuthorizedUser.objects.create(form = id_form, stu_list=row[0])
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
    if request.method == "POST":
        # ดึงค่า length จากแบบฟอร์ม
        length = request.POST.get('length')
        print(length)
        # ตรวจสอบว่าค่า length มีค่าหรือไม่ ถ้าไม่มีกำหนดค่าเป็น 1
        if length is None:
            length = 0
        
        # แปลงค่า length เป็น integer
        length = int(length)   

        # ดึงค่า main_field จากแบบฟอร์ม
        main_fields = request.POST.getlist('main_field[]')

        # สร้าง main PLOs และ sub PLOs จากข้อมูลที่รับมาจากแบบฟอร์ม
        for main_field in main_fields:
            main_plo = PLOs.objects.create(text=main_field) # สร้าง main PLOs
    
            for i in range(length):
                sub_field_name = f"sub_field_{i+1}[]"
                sub_field_value = request.POST.get(sub_field_name)  
                print(sub_field_value)
                
                if sub_field_value:
                    PLOs.objects.create(text=sub_field_value, parent=main_plo) # สร้าง sub PLOs
                else: None

        return HttpResponse("Data saved successfully!")

    return render(request, 'create_plos.html')

def manage_plos(request):
    plos = PLOs.objects.filter(parent__isnull=True)  # เลือกเฉพาะฟิลด์แม่โดยกรองให้ parent เป็น None
    return render(request, 'manage_plos.html', {'plos': plos})
