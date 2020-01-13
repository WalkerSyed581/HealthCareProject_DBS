from django.shortcuts import render, get_object_or_404, reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta

from.forms import *
from main.models import *
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect


# Create your views here.

def index(request, patient_id):

    patient = Patient.objects.get(pk=patient_id)

    request.session.set_expiry(0)

    if request.user.is_anonymous:
        return redirect('main:login')

    if request.user.email != patient.email:
        return HttpResponseRedirect(reverse('patient:index', args=(request.user.id,)))


    # add splice
    time_threshold = datetime.now()
    docAppointments = DoctorAppointment.objects.filter(patient = patient_id)

    docAppointments1 = DoctorAppointment.objects.filter(patient = patient_id,time__gte =  time_threshold)

    labAppointments = LabAppointment.objects.filter(patient = patient_id)

    labAppointments1 = LabAppointment.objects.filter(patient = patient_id,time__gte =  time_threshold)

    doctors = Doctor.objects.filter(pk__in = docAppointments.values_list('doctor'))
    doctors1 = Doctor.objects.filter(pk__in = docAppointments1.values_list('doctor'))

    conductors = HelpingStaff.objects.filter(pk__in = labAppointments.values_list('conducted_by'),role='ls')
    conductors1 = HelpingStaff.objects.filter(pk__in = labAppointments1.values_list('conducted_by'),role='ls')

    prescriptions = Prescription.objects.filter(appointment__in = docAppointments)
    drugs = Drug.objects.filter(prescription__in = prescriptions)
    supportGroups = SupportGroup.objects.filter(members = patient_id)
    supportGroupConductors = SupportGroupConductor.objects.filter(pk__in = supportGroups.values_list('conducted_by'))
    
   

    
    context = {"patient" : patient,"docAppointments": docAppointments,
        "docAppointments1": docAppointments1,"labAppointments":labAppointments,
        "doctors":doctors,"doctors1":doctors1,"conductors":conductors,
        "conductors1":conductors1,"prescriptions": prescriptions,
        "drugs":drugs,"supportGroups" : supportGroups,
        "supportGroupsConductors" : supportGroupConductors}
    return render(request, 'patient/index.html', context=context)

def bill(request, patient_id):
    patient = Patient.objects.get(patient_id)
    bill = Bill.objects.get(patient=patient_id)
    docAppointments = DoctorAppointment.objects.get(patient = patient_id)
    fees = Bill.calculate_fee(patient_id)

    context = {'patient':patient, 'bill':bill, 'docAppointments':docAppointments,"fees":fees}
    return render(request,'patient/bill.html',context=context)

def labReport(request, patient_id, lab_report_id):
    patient = Patient.objects.get(pk=patient_id)
    labReports = LabReport.objects.get(pk=lab_report_id)

    context = {
        'patient':patient,
        'labReports':labReports
    }   
    return render(request,'patient/labReport.html', context=context)

def getAppointment(request, patient_id):
    if request.method == 'POST':
        form = MakeAppointmentForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            
            DoctorAppointment.objects.create(patient=patient_id, time=timezone.datetime(), cancelled=False,**userObj)

            return HttpResponseRedirect(reverse('patient:index', args=(patient_id,)))
    
    else:
        form = MakeAppointmentForm()
        
    return render(request, 'patient/getData.html', {'form' : form})