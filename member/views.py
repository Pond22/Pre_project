from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from member.forms import RegisterForm
from django.contrib.auth.models import Group
# Create your views here.
def member(request):
    return HttpResponse("คน")

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request, 
            username=username, 
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/')
            
    return render(request, 'member/sign_in.html')

def sign_out(request):
    logout(request)
    return redirect('/member')
'''
def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()
        print(form)

    return render(request, 'member/sign_up.html', {'form': form})
'''
def sign_up(request: HttpResponse):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            x = user.email
            user.username = x[:x.index("@")]
           #user.username = user.email[:10] if user.email else ''  
            user.save()
            form.save()
            return redirect('/index')
    else:
        form = RegisterForm()
            
    context = {'form': form}
    return render(request, 'member/sign_up.html', context)

'''
แนวคิด

def import_users_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            email = row[0] + '@payap.ac.th'  
            password = row[0]  # ใช้คอลัมน์ที่ 0 เป็นรหัสผ่าน
            user = User.objects.create_user(username=email, email=email, password=password)
            group = Group.objects.get(name='นักศึกษา')
            user.groups.add(group)  # เพิ่มเข้ากลุ่มที่ 2

import_users_from_csv('/path/to/your/csv/file.csv') เรียกใช้

แบบนี้จะกำหนดกลุ่มผู้ใช้ (นักศึกษา) ทั้งหมดในทีเดียวโดยที่แต่ละฟอร์มที่เอามาลงจะสามารถตรวจสอบได้ว่านักศึกษาคนไหนมีสิทธิ์ในการประเมินแบบฟอร์มนี้และเป็นการสร้างผู้ใช้ใหม่ไปในตัว
'''