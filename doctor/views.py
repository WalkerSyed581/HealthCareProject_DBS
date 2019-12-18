from django.shortcuts import render

# Create your views here.

def index(request):
    # doctor = Doctor.objects.get(pk = doctor_id).full_name()
    # docAppointments = DoctorAppointment.objects.get(doctor = doctor_id)
    # patient = Patient.objects.get(pk = docAppointments.patient)
    # context = {"patient" : patient,"docAppointments": docAppointments,"doctorName":doctor}
    return render(request,'doctor/index.html')

def patientInfo(request):
    # Display old Appointments
    # docAppointments = DoctorAppointment.objects.get(doctor = doctor_id)

    # doctor = Doctor.objects.get(pk = doctor_id).full_name()
    # patient = Patient.objects.get(pk = patient_id)
    # context = {"patient" : patient,"docAppointments":docAppointments,"doctorName": doctor}
    return render(request,'doctor/patientInfo.html')

def appointmentReport(request):
    # labReport = LabReport.objects.get(appointment = appointment_id)
    # context = {"labReport" : labReport}
    return render(request,'doctor/appointmentReport.html')

