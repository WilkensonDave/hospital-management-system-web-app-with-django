from django.db import models
from userauthentication import models as userauths_models
from django.utils import timezone
# Create your models here.

NOTIFICATION_TYPE = (
    ("appointment scheduled", "appointment scheduled"),
    ("appointment cancelled", "appointment cancelled")
)


class Patient(models.Model):
    user = models.OneToOneField(userauths_models.User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile_image", 
        null=True, blank=True, default="userdefault.png")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    mobile = models.CharField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.CharField(max_length=200, null=True, blank=True)
    blood_group = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.full_name}"

class Notification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")
    appointment = models.ForeignKey("hospitalsystem.Appointement", on_delete=models.CASCADE, 
        null=True, blank=True, related_name="patient_appointement_notification")
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Notification"
    
    def __str__(self):
        return f"{self.patient.full_name} Notification"