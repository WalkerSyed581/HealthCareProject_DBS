from django.db import models

# Create your models here.

# Patient Table
class Patient(models.Model):

    name = models.CharField(max_length=50)

    # enter rest of the attributes


# Patient History

class MedicalHistory(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    summary = models.TextField(max_length=500)