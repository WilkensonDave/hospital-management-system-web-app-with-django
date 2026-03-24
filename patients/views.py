from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient, Notification
from hospitalsystem import models as base_model
from userauthentication import models as auth_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import models

@login_required
def patients_dashboard(request):
    patient = Patient.objects.get(user=request.user)
    appointments = base_model.Appointement.objects.filter(patient=patient)
    notifications = Notification.objects.filter(patient=patient)
    total_spent = base_model.Billing.objects.filter(patient=patient).aggregate(total_spent=models.Sum("total"))["total_spent"]
    context = {
        "appointments":appointments,
        "notifications":notifications,
        "patient":patient,
        "total_spent":total_spent
    }
    return render(request, "patient/dashboard.html", context)

@login_required 
def appointments(request):
    patient = Patient.objects.get(user=request.user)
    appointments = base_model.Appointement.objects.filter(patient=patient)
    context = {
        "appointments":appointments,
        "patient":patient
    }
    return render(request, "patient/appointments.html", context)

@login_required 
def appointment_details_patients(request, appointment_id):
    patient = Patient.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(patient=patient, appointment_id=appointment_id)
    medical_records = base_model.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_model.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_model.Prescription.objects.filter(appointment=appointment)
    context = {
        "appointments":appointment,
        "medicalrecords":medical_records,
        "lab_tests":lab_tests,
        "prescriptions":prescriptions
    }
    
    return render(request, "patient/appointment-details.html", context)

@login_required
def cancel_appointment(request, appointment_id):
    patient = Patient.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, patient=patient)
    appointment.status = "cancelled"
    appointment.save()
    messages.success(request, "Your appointment has been cancelled")
    return redirect("appointment_details_patients", appointment_id)

@login_required 
def activate_appointment(request, appointment_id):
    patient = Patient.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, patient=patient)
    appointment.status = "scheduled"
    appointment.save()
    messages.success(request, "Your appointment has been changed")
    return redirect("appointment_details_patients", appointment_id)

@login_required
def patient_notifications(request):
    patient = Patient.objects.get(user=request.user)
    notifications = Notification.objects.filter(patient=patient, seen=False)
    context = {
        "notifications":notifications,
        "patient":patient
    }
    return render(request, "patient/notifications.html", context)



@login_required
def payments_details(request):
    patient = Patient.objects.get(user=request.user)
    payments = base_model.Billing.objects.filter(appointment__patient=patient, status="Paid")
    context = {
        "payments":payments,
        "patient":patient
    }
    return render(request, "patient/payments.html", context)


@login_required
def patient_notification_seen(request, id):
    patient = Patient.objects.get(user=request.user)
    notifications = Notification.objects.get(patient=patient, id=id)
    notifications.seen = True
    notifications.save()
    
    messages.success(request, "Notification has been seen")
    return redirect("payments_details")

@login_required
def edit_patient_profile(request):
    patient = Patient.objects.get(user=request.user)
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("date_of_birth")
        blood_group = request.POST.get("blood_group")
        gender = request.POST.get("gender")
        
        patient.full_name = full_name
        patient.user.email = email
        patient.mobile = mobile
        patient.address = address
        patient.date_of_birth = date_of_birth
        patient.blood_group = blood_group
        patient.gender = gender
        
        try:
            image = request.FILES["image"]
            patient.profile_image = image
        except Exception:
            pass
        patient.save()
        messages.success(request, "Profile has been successfully updated.")
        return redirect("patients-dashboard")
    
    context = {
        "patient":patient
    }
    return render(request, "patient/patient-profile.html", context)

def about_us(request):
    return render(request, "userauth/about-us.html")

def contact_us(request):
    return render(request, "userauth/contact-us.html")

@login_required
def medical_reports(request):
    patient = Patient.objects.get(user=request.user)
    medical_reports = base_model.MedicalRecord.objects.filter(appointment__patient=patient)
    context = {
        "medical_reports":medical_reports,
        "patient":patient
    }
    
    return render(request, "patient/medical-reports.html", context)

@login_required
def lab_tests(request):
    patient = Patient.objects.get(user=request.user)
    lab_tests = base_model.LabTest.objects.filter(appointment__patient=patient)
    
    context = {
        "lab_tests":lab_tests,
        "patient":patient
    }
    return render(request, "patient/lab-test.html", context)

@login_required
def patient_prescription(request):
    patient = Patient.objects.get(user=request.user)
    prescriptions = base_model.Prescription.objects.filter(appointment__patient=patient)
    context = {
        "prescriptions":prescriptions,
        "patient":patient,
    }
    return render(request, "patient/prescription.html", context)