from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        
        else:
            messages.warning(request,'Username or password is incorrect')
            return redirect('login')
        
    else:
         return render(request,'authenticate/login.html')

def success_user(request):
    return render(request,'authenticate/success.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('login')