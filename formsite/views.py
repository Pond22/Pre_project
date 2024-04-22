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
        
        le = request.POST.get('length')
        if le is None:
            le = 1
        else:
            le = int(le)

        print(le)
          
        for i in range(0, le+1):
            name_main = 'main_field' + str(i)
                
            main_fields = request.POST.get(name_main)  # รับข้อมูลจากฟิลด์แม่
            print(main_fields)
            main_field = PLOs.objects.create(text=main_fields)
            
            name_sub = 'sub_field_' + str(name_main)
            sub_fields = request.POST.getlist(name_sub)
            print(sub_fields)
            print(name_sub)
            #PLOs.objects.create(text=sub_fields, parent=main_field)
       
            # วนลูปผ่านฟิลด์ลูกและสร้าง PLO ลูก
            for sub_field_text in sub_fields:
                sub_field = PLOs.objects.create(text=sub_field_text, parent=main_field)

        return HttpResponse("Data saved successfully!")

    return render(request, 'create_plos.html')


def manage_plos(request):
    if request.method == 'POST':
        plo_id = request.POST.get('plo_id')
        new_text = request.POST.get('main_text')
        sub_item_id = request.POST.get('sub_item_id')
        sub_text = request.POST.get('sub_text')

        try:
            if plo_id:  
                plo = get_object_or_404(PLOs, id=plo_id)
                plo.text = new_text
                plo.save()
                return redirect('manage_plos')
            elif sub_item_id:  
                sub_plo = get_object_or_404(PLOs, id=sub_item_id)
                sub_plo.text = sub_text
                sub_plo.save()
                return redirect('manage_plos')
            else:
                return HttpResponse("Invalid form data.")
        except PLOs.DoesNotExist:
            return HttpResponse("PLO or sub-item does not exist.")
    else:
        plos = PLOs.objects.filter(parent__isnull=True)
        return render(request, 'manage_plos.html', {'plos': plos})

'''
def manage_plos(request):
    if request.method == 'POST':
        plo_id = request.POST.get('plo_id')
        new_text = request.POST.get('main_text')
   
        # ตรวจสอบว่ามี PLOs ในฐานข้อมูลหรือไม่ ถ้าไม่มีจะให้กลับไปที่หน้าเดิม
        plo = get_object_or_404(PLOs, id=plo_id)

        # อัปเดตข้อมูล PLO ในฐานข้อมูล
        plo.text = new_text
        plo.save()

        return redirect('manage_plos')

    else:
        plos = PLOs.objects.filter(parent__isnull=True)
        return render(request, 'manage_plos.html', {'plos': plos})'''