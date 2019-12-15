from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'doctor/index.html')

def patientInfo(request):
    return render(request,'doctor/patientInfo.html')

def appointmentReport(request):
    return render(request,'doctor/appointmentReport.html')

