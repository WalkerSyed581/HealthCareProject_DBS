from django.shortcuts import render, get_object_or_404
from django.utils import timezone


# Create your views here.

def index(request):
    return render(request,'patient/index.html')

def bill(request):
    return render(request,'patient/bill.html')

def labReport(request):
    return render(request,'patient/labReport.html')