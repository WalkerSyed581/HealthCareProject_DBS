from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from.managers import CustomUserManager

# Create your models here.

class User(AbstractUser):
    """
    Base User class
    """
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()
    address = models.CharField(max_length=100, null=True)

    MALE = 'm'
    FEMALE = 'f'
    NONE = 'n'
    genders = [(MALE, 'male'),
                (FEMALE, 'female'),
                (NONE, 'None'),]

    gender = models.CharField(max_length=1, choices=genders, default=NONE)
    phone = models.CharField(max_length=11, null=True)
    cnic = models.CharField(max_length=15, null=True)
    age = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

class Staff(User):
    '''
    Basic Staff class for all employees
    '''
    joining_date = models.DateTimeField()
    salary = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

class Doctor(Staff):
    '''
    Doctor Class
    '''
    specialization = models.CharField(max_length=100, null=True)
    fee = models.PositiveIntegerField(default=0)
    starting_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

class SupportGroupConductor(Staff):
    

    class Meta:
        verbose_name = "Support Group Conductor"

class HelpingStaff(Staff):
    '''
    Helping Staff Class for lab and ward staff
    '''
    WARD_STAFF = 'ws'
    LAB_STAFF = 'ls'
    RECEPTIONIST = 'rc'
    NONE = 'n'

    roles = [
        (WARD_STAFF, "Ward Staff"),
        (LAB_STAFF, "Lab Staff"),
        (NONE, "None"),
    ]
    role = models.CharField(max_length=2, choices=roles, default=NONE)

    class Meta:
        verbose_name = "Helping Staff"
        verbose_name_plural = "Helping Staff"

class Patient(User):
    '''
    Patient Class
    '''
    emergency_contact = models.CharField(max_length=11, null=True)

    doctor_appointments = models.ManyToManyField(Doctor, through='DoctorAppointment')
    Lab_appointments = models.ManyToManyField(HelpingStaff, through='LabAppointment')

    class Meta:
        verbose_name = "Patient"

class Appointment(models.Model):

    notes = models.CharField(max_length=200, null=True)
    cancelled = models.BooleanField(default=False)
    time = models.DateTimeField()

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.first_name + " Appointment" + self.time.__str__()

    class meta:
        abstract = True
        verbose_name = "Appointment"

class DoctorAppointment(Appointment):
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Doctor Appointment"

class LabAppointment(Appointment):
    conducted_by = models.ForeignKey(HelpingStaff, on_delete=models.CASCADE, null=True)
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE, null=True)
    test_id = models.ForeignKey('LabTest',on_delete=models.CASCADE,null=True)
    
    class Meta:
        verbose_name = "Lab Appointment"

class LabReport(models.Model):

    text = models.TextField(max_length=2000)

    appointment = models.ForeignKey(LabAppointment, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lab Report"

class Drug(models.Model):
    prescription  = models.ForeignKey('Prescription', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dose = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Drug"

class Prescription(models.Model):

    appointment = models.OneToOneField(DoctorAppointment, on_delete=models.CASCADE)
    tests = models.ManyToManyField('LabTest')
    conditions = models.TextField(max_length=500, null=True)
    notes = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.appointment.__str__() + " Prescription"

    class Meta:
        verbose_name = "Prescription"

class Ward(models.Model):
    
    capacity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "Ward {}".format(self.id)

    class Meta:
        verbose_name = "Ward"

class Admission(models.Model):

    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    attendant = models.ForeignKey(HelpingStaff, on_delete=models.CASCADE)

    from_date = models.DateTimeField()

    number_of_days = models.PositiveIntegerField(default=1)
    discharged = models.BooleanField(default=False)

    def __str__(self):
        return self.patient.__str__() + " admission"


    class Meta:
        verbose_name = "Admission"

class SupportGroup(models.Model):
    MONDAY = 'mon'
    TUESDAY = 'tue'
    WEDNESDAY = 'wed'
    THURSDAY = 'thu'
    FRIDAY = 'fri'
    SATURDAY = 'sat'
    SUNDAY = 'sun'

    days = [
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
    ]

    name = models.CharField(max_length=50, default="Support Group Generic")
    timing = models.TimeField()
    day = models.CharField(max_length=3, choices=days, default=MONDAY)
    description = models.TextField(max_length=1000, null=True)
    fee = models.PositiveIntegerField(default=0)


    conducted_by = models.ManyToManyField(SupportGroupConductor)
    members = models.ManyToManyField(Patient)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Support Group"

class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_appointment = models.ForeignKey(DoctorAppointment, on_delete=models.CASCADE, null=True)
    lab_appointment = models.ForeignKey(LabAppointment, on_delete=models.CASCADE, null=True)
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, null=True)



    def calculate_fee(self,patient_id):
        allDues = Bill.objects.filter(patient = patient_id)
        docAppointments = DoctorAppointment.objects.filter(pk__in = allDues.values_list('doctor_appointment'))
        doctors = Doctor.objects.filter(pk__in = docAppointments.values_list('doctor'))
        doctorFee = 0
        for docAppointment in docAppointments:
            for doctor in doctors:
                if docApppointment.doctor == doctor.id:
                    doctorFee += doctor.fee

        labAppopintments = LabAppointment.objects.filter(pk__in = allDues.values_list('lab_appointmnet'))
        patientTests = Prescription.objects.values_list(tests,pk__in = labAppopintments.values_list('prescription'))
        testFees = None
        totalTestFee = 0
        for patientTest in patientTests:
            test = LabTest.objects.get(pk__in = patientTests)
            testFees[test.name].append(test.fee)
            totalTestFee += test.fee

        supportGroupFees = SupportGroup.objects.filter(fee,members__id = patient_id)

        totalSupportGroupFee = 0
        for supportGroupFee in supportGroupFees:
            totalSupportGroupFee += supportGroupFee

        totalFee = doctorFee + totalTestFee + totalSupportGroupFee
        
        return {"doctorFee": doctorFee,"testFees":testFees,"totalTestFee":totalTestFee,"supportGroupFee":totalSupportGroupFee,"totalFee": totalFee}
        


    class Meta:
        verbose_name = "Bill"

class LabTest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    fee = models.PositiveIntegerField(default=0)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Lab Test"

class Service(models.Model):
    
    name = models.CharField(max_length=100)

    description = models.TextField(max_length=1000)

    picture = models.ImageField(upload_to='static')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Service"