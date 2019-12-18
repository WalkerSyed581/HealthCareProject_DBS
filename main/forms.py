from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Patient

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class PatientRegistrationForm(forms.ModelForm):

    class Meta:
        model = Patient

        fields = ['email', 'first_name', 'last_name',
                 'password', 'gender', 'phone', 'age',
                 'cnic', 'emergency_contact']
