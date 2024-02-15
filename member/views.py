from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from member.forms import RegisterForm
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
            # Log user in
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
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()
            
    context = {'form': form}
    return render(request, 'member/sign_up.html', context)
