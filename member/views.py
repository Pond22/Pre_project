from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from member.forms import RegisterForm
from django.contrib.auth.models import Group, User
from formsite.models import *
import re
from formsite.user_detect import*
from django.http import JsonResponse
# Create your views here.
def clean_string(value):
    return re.sub(r'\s+', '', value)

@login_required(login_url="sign_in") 
@admin_required
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
            
            Form.objects.filter(created_by=user).update(created_by=None)
            CommentForm.objects.filter(respondent=user).update(respondent=None)
            AssessmentResponse.objects.filter(respondent=user).update(respondent=None)
            Teamplates.objects.filter(created_by=user).update(created_by=None)
            
            user.delete()
            return redirect('/manage_member')
        
    
    return render(request, 'member/manage_member.html', {'user_profile': user_profile, 'users_in_department':users_in_department})

def sign_in(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return redirect('/index')
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

def add_teacher(request):
    if request.method == 'POST':
        first_id = request.POST.get('first_id')
        prefix_name = request.POST.get('prefix_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        department = request.POST.get('department')

        if first_id and prefix_name and first_name and last_name and email and department:
            tem_po = get_object_or_404(Departments, id=department)
            user = User.objects.create_user(username=first_id, email=email, first_name=first_name, last_name=last_name, password=first_id)
            group = Group.objects.get(name='อาจารย์')
            user.groups.add(group)
            user_profile = UserProfile.objects.create(user=user, prefix=prefix_name, department=tem_po)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'กรุณากรอกข้อมูลให้ครบถ้วน'})
    return JsonResponse({'success': False, 'error': 'เฉพาะคำขอแบบ POST เท่านั้น'})