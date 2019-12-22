from django import forms
from main.models import *
from django.contrib import messages


class MakeAppointmentForm(forms.ModelForm):

    class Meta:
        model = DoctorAppointment

        fields = '__all__'

        exclude = ['cancelled', 'patient']