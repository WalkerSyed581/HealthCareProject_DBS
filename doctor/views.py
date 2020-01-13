from django.shortcuts import render, get_object_or_404, reverse

from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from main.models import *


# Create your views here.

def index(request, doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)

    request.session.set_expiry(0)

    if request.user.is_anonymous:
        return redirect('main:login')

    if request.user.email != doctor.email:
        return HttpResponseRedirect(reverse('doctor:index', args=(request.user.id,)))

    time_threshold = datetime.now()

    patient = None
    docAppointments = None
    try:
        docAppointments = DoctorAppointment.objects.get(doctor = doctor_id,time__gte = time_threshold).order_by('-time')
        patient = Patient.objects.get(pk = docAppointments.patient)
    except:
        pass
    
    context = {"patient" : patient,"docAppointments": docAppointments,"doctor":doctor}
    return render(request,'doctor/index.html',context)

def patientInfo(request,doctor_id,patient_id):
    # Display old Appointments
    time_threshold = datetime.now()
    docAppointments = DoctorAppointment.objects.get(patient = patient_id,time__lte = time_threshold)

    doctor = Doctor.objects.get(pk = doctor_id).full_name()
    patient = Patient.objects.get(pk = patient_id)
    context = {"patient" : patient,"docAppointments":docAppointments,"doctorName": doctor}
    return render(request,'doctor/patientInfo.html',context)

def labReports(request,doctor_id,patient_id,appointment_id):
    prescriptions = Prescription.objects.get(appointment = appointment_id)
    labAppointments = LabAppointment.objects.filter(prescriptions__in = prescriptions.id)
    labReports = LabReport.objects.filter(appointment__in = labAppointments.values_list('id'))
    conductors = HelpingStaff.objects.filter(pk__in = labAppointments.values_list('conducted_by'),role='ls')
    tests = LabTest.objects.filter(pk__in = labAppointments.values_list('test_id'))
    doctor = Doctor.objects.get(pk = doctor_id).full_name()
    patient = Patient.objects.get(pk = patient_id)
    context = {"patient" : patient,"doctorName": doctor,"tests":tests,"prescriptions":prescriptions,"labAppointments":labAppointments,"tests":tests,"conductors":conductors,"labReports":labReports}
    return render(request,'doctor/appointmentReport.html',context)

