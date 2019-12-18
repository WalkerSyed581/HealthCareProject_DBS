from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def index(request):
    return render(request,'main/index.html')

def about(request):
    return render(request,'main/about.html')

def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            
            return redirect('patient:index')
    else:
        form = AuthenticationForm()
    return render(request,'main/login.html', {'form':form})

def register(request):
    return render(request,'main/register.html')