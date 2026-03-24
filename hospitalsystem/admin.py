from django.contrib import admin
from hospitalsystem import models

class AppointmentInline(admin.TabularInline):
    model = models.Appointement
    extra = 1

class MedicalRecordInline(admin.TabularInline):
    model = models.MedicalRecord
    extra = 1

class LabTestInline(admin.TabularInline):
    model = models.LabTest
    extra = 1

class PrescriptionInline(admin.TabularInline):
    model = models.Prescription
    extra = 1

class BillingInline(admin.TabularInline):
    model = models.Billing
    extra = 1

class SeriveAdmin(admin.ModelAdmin):
    list_display = ["name", "cost"]
    search_fields = ["name", "description"]
    filter_horizontal = ["available_doctors"]

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["patient", "doctor", "appointment_date", "status"]
    search_fields = ["patien__user__username", "doctor__user__username"]
    inlines = [MedicalRecordInline, LabTestInline, PrescriptionInline, BillingInline]

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ["appointment", "diagnosis"]
    
class LabTestAdmin(admin.ModelAdmin):
    list_display = ["appointment", "test_name"]

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ["appointment", "medications"]

class BillingAdmin(admin.ModelAdmin):
    list_display = ["patient", "total", "status", "date"]


admin.site.register(models.Service, SeriveAdmin)
admin.site.register(models.Appointement, AppointmentAdmin)
admin.site.register(models.Billing, BillingAdmin)
admin.site.register(models.Prescription, PrescriptionAdmin)
admin.site.register(models.MedicalRecord, MedicalRecordAdmin)
admin.site.register(models.LabTest, LabTestAdmin)