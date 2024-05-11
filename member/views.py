from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from member.forms import RegisterForm
from django.contrib.auth.models import Group, User
from formsite.models import TemplateData, AssessmentItem, Teamplates, UserProfile, AuthorizedUser
import re
# Create your views here.
def clean_string(value):
    return re.sub(r'\s+', '', value)

def manage_member(request):
    user_profile = get_object_or_404(UserProfile, user=request.user) #คิวรี่แอดมินที่เข้าหน้านั้นตอนนั้นมาหาสาขา
    group = Group.objects.get(name="อาจารย์")
    users_in_department = UserProfile.objects.filter(department__name=user_profile.department, user__groups=group) #ค้นหาอาจารย์ที่อยู่ในสาขานั้นๆ กับแอดมิน
    
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')

        if action == 'edit':
            # ดึง user profile
            user_profile = get_object_or_404(UserProfile, user__id=user_id)
            user = user_profile.user

            # ใช้ฟังก์ชัน clean_string เพื่อ clean ข้อมูล
            user.username = clean_string(request.POST.get('username', ''))
            user.first_name = clean_string(request.POST.get('first_name', ''))
            user.last_name = clean_string(request.POST.get('last_name', ''))
            user.email = clean_string(request.POST.get('email', ''))
            user.save()

            user_profile.prefix = clean_string(request.POST.get('prefix', ''))
            user_profile.save()

            return redirect('/manage_member')


        elif action == 'delete':
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return redirect('/manage_member')
        
    
    return render(request, 'member/manage_member.html', {'user_profile': user_profile, 'users_in_department':users_in_department})

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