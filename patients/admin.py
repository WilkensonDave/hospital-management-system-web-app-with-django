from django.contrib import admin
from patients import models
# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ["appointment"]
    
admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Notification, NotificationAdmin)