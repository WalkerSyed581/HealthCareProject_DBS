from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'main/index.html')

def about(request):
    return render(request,'main/about.html')

def login(request):
    return render(request,'main/login.html')

def register(request):
    return render(request,'main/register.html')