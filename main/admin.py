from django.contrib import admin
from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import *


# Register your models Here

class CustomUserAdmin(User):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email',)

# admin.site.register(User)
admin.site.register(CustomUserAdmin)
admin.site.register(Staff)
admin.site.register(Doctor)
admin.site.register(SupportGroupConductor)
admin.site.register(HelpingStaff)
admin.site.register(Patient)
admin.site.register(Ward)
admin.site.register(Admission)
admin.site.register(Service)

admin.site.register(DoctorAppointment)
admin.site.register(LabTest)
admin.site.register(Prescription)

admin.site.register(SupportGroup)