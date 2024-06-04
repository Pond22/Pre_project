from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from member.forms import RegisterForm
from django.contrib.auth.models import Group, User
from formsite.models import *
import re
from formsite.user_detect import*
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
import json

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
    else:
            
        for data in users_in_department:
            print('check', data.user.username)
            groups = data.user.groups.all()  
            for group in groups:
                print('check', group.name)
    
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

            # Check the user's group and redirect accordingly
            if user.groups.filter(name='หัวหน้าสาขา').exists():
                return redirect('/manage_template')
            elif user.groups.filter(name='กรรมการ').exists():
                return redirect('/report_main')
            else:
                return redirect('/evaluate/')
            
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
def sign_in(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='หัวหน้าสาขา').exists():
            return redirect('/manage_template')
        elif request.user.groups.filter(name='กรรมการ').exists():
            return redirect('/report_main')
        else:
            return redirect('/evaluate/')

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

            # Check the user's group and redirect accordingly
            if user.groups.filter(name='หัวหน้าสาขา').exists():
                return redirect('/manage_template')
            elif user.groups.filter(name='กรรมการ').exists():
                return redirect('/report_main')
            else:
                return redirect('/evaluate/')

    return render(request, 'member/sign_in.html')

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

def update_user_group(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            group_name = data.get("group_name")
            action = data.get("action") 
            print(group_name)

            user = get_object_or_404(User, id=user_id)
            print(user)
            group = Group.objects.get(name=group_name)

            if action == 'add':
                user.groups.add(group)
            elif action == 'remove':
                user.groups.remove(group)

            user.save()
            return JsonResponse({'status': 'success'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Group.DoesNotExist:
            return JsonResponse({'error': 'Group not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def transfer_role(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_now = request.user

        if not user_now.groups.filter(name='หัวหน้าสาขา').exists():
            return JsonResponse({'success': False, 'error': 'You do not have permission to perform this action.'}, status=403)

        user = get_object_or_404(User, id=data.get("user_id"))
        admin = get_object_or_404(User, id=data.get("admin_id"))
        print('adminNow', admin.username)
        print('target', user.username)
        group = get_object_or_404(Group, name='หัวหน้าสาขา')
        
        if admin.groups.filter(name='หัวหน้าสาขา').exists():
            admin.groups.remove(group)
        
        user.groups.add(group)
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
        
    
def update_line_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            line_token = data.get("line_token")
            
            if len(line_token) != 43:
                return JsonResponse({'error': 'Invalid line token format'}, status=400)

            if not user_id or not line_token:
                return JsonResponse({'error': 'Missing parameters'}, status=400)

            user_profile = get_object_or_404(UserProfile, user__id=user_id)
            user_profile.line_token = line_token
            user_profile.save()

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)