from django.db import models
from userauthentication import models as userauths_models
from django.utils import timezone
# Create your models here.

NOTIFICATION_TYPE = (
    ("new appointment", "new appointment"),
    ("appointment cancelled", "appointment cancelled")
)


class Doctor(models.Model):
    user = models.OneToOneField(userauths_models.User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile_image", 
        null=True, blank=True, default="userdefault.png")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True)
    mobile = models.CharField(max_length=500, null=True, blank=True)
    headline = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    specialization = models.CharField(max_length=200, null=True, blank=True)
    qualification = models.CharField(max_length=200, null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    next_available_appointement_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    
    def __str__(self):
        return f"Dr. {self.full_name}"

class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")
    appointment = models.ForeignKey("hospitalsystem.Appointement", on_delete=models.CASCADE, 
        null=True, blank=True, related_name="doctor_appointement_notification")
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Notification"
    
    def __str__(self):
        return f"Dr {self.doctor.full_name} Notification"

