from django.contrib import admin

# Register your models here.
from .models import Doctor, Patient, Appointment, Specialization

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Specialization)