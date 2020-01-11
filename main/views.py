from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django import forms

from .models import User, Doctor, Patient, HelpingStaff, Service, SupportGroupConductor
from .forms import PatientRegistrationForm
# Create your views here.

def index(request):
    services = Service.objects.all()[:5]
    return render(request,'main/index.html', {'services':services})

def about(request):
    return render(request,'main/about.html')

def loginView(request):
    '''
        Login View

        Issues: Only way to create new staff members is through admin 
        and it does not automatically hash passwords
    '''
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login_detail = form.cleaned_data
            print(form.cleaned_data)
            user = authenticate(request, username=login_detail['username'], password=login_detail['password'])
            if user is not None:
                login(request, user)
            try:
                if (Doctor.objects.get(email=login_detail['username'])):
                    return redirect('doctor:index')
            except ObjectDoesNotExist:
                print("User is not a Doctor")

            try:
                patient = Patient.objects.get(email=login_detail['username'])

                return HttpResponseRedirect(reverse('patient:index', args=(patient.id,)))
            except ObjectDoesNotExist:
                print("User is not a Patient")

            try:
                if (HelpingStaff.objects.get(email=login_detail['username'])):
                    return redirect('helping_staff:index')
            except ObjectDoesNotExist:
                print("User is not a Helper")

            try:
                if (SupportGroupConductor.objects.get(email=login_detail['username'])):
                    return redirect('helping_staff:index')
            except ObjectDoesNotExist:
                print("User is not a Support Group Conductor")

            try:
                if (User.objects.get(email=login_detail['username']).is_superuser 
                    or User.objects.get(email=login_detail['username']).is_staff):
                    return redirect('/admin')
            except ObjectDoesNotExist:
                print("User is not an Admin")
            
            return redirect('main:index')
    else:
        form = AuthenticationForm()
    return render(request,'main/login.html', {'form':form})


def register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            
            if not (User.objects.filter(email=userObj['email']).exists()):
                Patient.objects.create_user(email=userObj['email'], password=userObj['password'], first_name=userObj['first_name'], last_name=userObj['last_name'], gender=userObj['gender'], age=userObj['age'], cnic=userObj['cnic'], emergency_contact=userObj['emergency_contact'])
                user = authenticate(email = userObj['email'], password = userObj['password'])
                login(request, user)
                patient = Patient.objects.get(email=userObj['email'])

                return HttpResponseRedirect(reverse('patient:index', args=(patient.id,)))
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
                
    else:
        form = PatientRegistrationForm()
        
    return render(request, 'main/register.html', {'form' : form})


