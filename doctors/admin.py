from django.contrib import admin
from doctors import models
# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', "specialization", "qualification", "years_of_experience"]

class NotificationAdmin(admin.ModelAdmin):
    list_display = ["doctor", "appointment", "type", "seen", "date"]
    
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Notification, NotificationAdmin)