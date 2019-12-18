from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django import forms

from .models import User, Doctor, Patient, HelpingStaff
from .forms import PatientRegistrationForm
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
            
            try:
                if (Doctor.objects.get(email=form.username_field)):
                    return redirect('doctor:index')
            except ObjectDoesNotExist:
                pass

            try:
                if (Patient.objects.get(email=form.username_field)):
                    return redirect('patient:index')
            except ObjectDoesNotExist:
                pass

            try:
                if (HelpingStaff.objects.get(email=form.username_field)):
                    return redirect('helping_staff:index')
            except ObjectDoesNotExist:
                pass
            
            if user.is_staff or user.is_superuser:
                redirect('/admin')
            return redirect('main:index')
    else:
        form = AuthenticationForm()
    return render(request,'main/login.html', {'form':form})

def register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            # username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(email=email).exists()):
                Patient.objects.create_user(email=email, password=password, )
                user = authenticate(email = email, password = password)
                login(request, user)
                return redirect("patient:index")   
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
                
    else:
        form = PatientRegistrationForm()
        
    return render(request, 'main/register.html', {'form' : form})