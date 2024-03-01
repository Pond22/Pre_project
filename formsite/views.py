from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from .models import *
from .models import form as form_id
import time
import pandas as pd
from evaluate.forms import PLOsForm, Form, ClosForm, CSVUploadForm, Aut
from django.contrib.auth.models import User, Group
# Create your views here.

#def index(request):
    #return render(request, '/index.html')

def home(request):
    #x = form.objects.filter(id__range=(1,4), name__in=("วิชาภาษาไทย", "วิชาภาษาซี"))
    x  = form.objects.filter(class_code__in=("se211", "SE5555"))
    return render(request, 'home.html', {'data': x})

def index(request):
    return render(request, 'index.html')

def view_form(request):
    if request.method == 'POST':
        #form = RegisterForm(request.POST)
        form = CSVUploadForm(request.POST, request.FILES)
        use_aut = Aut(request.POST)
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
                        user.groups.add(group)  # เพิ่มเข้ากลุ่มที่ 2
                    except :
                        #print("ซ้ำ",index )
                        None
                    AuthorizedUser.objects.create(form = id_form, stu_list=row[0])
                    processed_records +=1
        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution time:", execution_time, "seconds")
                
    csv_1 = CSVUploadForm()
    context = {'csv_1': csv_1}
    return render(request, 'test.html', context)

