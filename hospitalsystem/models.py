from django.db import models
from shortuuid.django_fields import ShortUUIDField
from patients import models as patient_models
from doctors import models as doctor_models

class Service(models.Model):
    image = models.ImageField(upload_to="featured_image", default="default.jpg", null=True, blank=True)
    name =  models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available_doctors = models.ManyToManyField(doctor_models.Doctor, blank=True)
    
    
    def __str__(self):
        return f"{self.name} - {self.cost}"


class Appointement(models.Model):
    STATUS = [
        ("scheduled", "scheduled"),
        ("completed", "completed"),
        ("pending", "pending"),
        ("cancelled", "cancelled")
    ]
    
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True,
        blank=True, related_name="service_appointment")
    
    doctor = models.ForeignKey(doctor_models.Doctor, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="doctor_appointment")
    
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="patient_appointment")
    
    appointment_date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    appointment_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    status = models.CharField(max_length=120, choices=STATUS)
    
    def __str__(self):
        return f"{self.patient.full_name} with {self.doctor.full_name}"

class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointement, on_delete=models.CASCADE, related_name="medicalrecord")
    diagnosis = models.TextField()
    treatment = models.TextField()
    
    def __str__(self):
        return f"Medical Record for {self.appointment.patient.full_name}"


class LabTest(models.Model):
    appointment = models.ForeignKey(Appointement, on_delete=models.CASCADE, related_name="labtest")
    test_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.test_name}"

    
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointement, on_delete=models.CASCADE, related_name="prescription")
    medications = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Prescription for {self.appointment.patient.full_name}"


class Billing(models.Model):
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="patient_billing")
    
    appointment = models.ForeignKey(Appointement, on_delete=models.CASCADE, 
        related_name="appointment_billing", blank=True, null=True)
    
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=120, choices=[("Paid", "Paid"), ("Unpaid", "Unpaid")])
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Billing for {self.patient.full_name} - Total: {self.total}"