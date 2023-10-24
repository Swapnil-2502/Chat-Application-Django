from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

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

def register_user(request):
    
    form = UserCreationForm(request.POST)
    
    if form.is_valid():
        form.save()
        
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username,password=password)
        login(request,user)
        messages.success(request,'Your registration was successfull')
        return redirect('home')
    
    else:
        form = UserCreationForm()
    
    return render(request, 'authenticate/register.html',{'form':form})