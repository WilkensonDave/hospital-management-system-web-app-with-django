from django.shortcuts import render
from django.http import HttpResponse
from .models import Doctor, Notification
from hospitalsystem import models as base_model
from userauthentication import models as auth_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
# Create your views here.


@login_required
def dashboard(request):
    doctor = Doctor.objects.get(user=request.user)
    appointments = base_model.Appointement.objects.filter(doctor=doctor)
    notification = Notification.objects.filter(doctor=doctor)
    context = {
        "appointments":appointments,
        "notifications":notification,
        "doctor":doctor
    }
    
    return render(request, "doctor/dashboard.html", context)

@login_required
def appointments(request):
    doctor = Doctor.objects.get(user=request.user)
    appointments = base_model.Appointement.objects.filter(doctor=doctor)
    
    context = {
        "doctor":doctor,
        "appointments":appointments
    }
    
    return render(request, "doctor/appointments.html", context)


@login_required
def appointment_details(request, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, doctor=doctor)
    medical_records = base_model.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_model.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_model.Prescription.objects.filter(appointment=appointment)
    
    context = {
        "appointment":appointment,
        "medical_records":medical_records,
        "lab_tests":lab_tests,
        "prescriptions":prescriptions,
        "doctor":doctor
    }
    
    return render(request, "doctor/appointment-details.html", context)

@login_required
def cancel_appointment(request, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = "cancelled"
    appointment.save()
    messages.success(request, "Appointment has been successfully cancelled.")
    return redirect("appointment_details", appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = "scheduled"
    appointment.save() 
    messages.success(request, "Appointment has been successfully scheduled")
    return redirect("appointment_details", appointment.appointment_id)


@login_required
def complete_appointment(request, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = "completed"
    appointment.save()
    messages.success(request, "Appointment has been completed")
    return redirect("appointment_details", appointment.appointment_id)


@login_required
def add_medical_report(request, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, doctor=doctor)
    
    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        
        medical = base_model.MedicalRecord.objects.create(diagnosis=diagnosis, treatment=treatment, appointment=appointment)
        medical.save()
    messages.success(request, "Medical report has been successfully added")
    return redirect("appointment_details", appointment.appointment_id)
        
@login_required
def edit_medical_report(request, appointment_id, medical_report_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, doctor=doctor)
    medical_report = base_model.MedicalRecord.objects.get(id=medical_report_id, appointment=appointment)
    
    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        medical_report.diagnosis = diagnosis
        medical_report.treatment = treatment
        medical_report.save()
    messages.success(request, "Medical report has been updated")
    return redirect("appointment_details", appointment.appointment_id)

@login_required
def add_lab_test_report(request, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, doctor=doctor)
    
    if request.method == "POST":
        test_name = request.POST.get("test_name")
        description = request.POST.get("description")
        result  = request.POST.get("result")
        
        lab_test = base_model.LabTest.objects.create(appointment=appointment, 
            test_name=test_name, description=description, result=result)
        lab_test.save()
        
    messages.success(request, "Lab test has been successfully added")
    return redirect("appointment_details", appointment.appointment_id)
    

@login_required
def edit_lab_test_report(request, appointment_id, lab_test_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, doctor=doctor)
    lab_test = base_model.LabTest.objects.get(id=lab_test_id, appointment=appointment)
    
    if request.method == "POST":
        test_name = request.POST.get("test_name")
        description = request.POST.get("description")
        lab_test.test_name = test_name
        lab_test.description = description
        lab_test.save()
    messages.success(request, "Lab test has been updated")
    return redirect("appointment_details", appointment.appointment_id)

@login_required
def add_prescription(request, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, doctor=doctor)
    
    if request.method == "POST":
        medications = request.POST.get("medications")
        
        medications = base_model.Prescription.objects.create(appointment=appointment, medications=medications)
        medications.save()
    
    messages.success(request, "Prescription has been successfully created")
    return redirect("appointment_details", appointment.appointment_id)

@login_required
def edit_prescription(request, appointment_id, prescription_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = base_model.Appointement.objects.get(appointment_id=appointment_id, doctor=doctor)
    prescriptions = base_model.Prescription.objects.get(id=prescription_id, appointment=appointment)
    
    if request.method == "POST":
        medications = request.POST.get("medications")
        prescriptions.medications = medications
        prescriptions.save()
        
    messages.success(request, "Prescription has been updated")
    return redirect("appointment_details", appointment.appointment_id)

@login_required
def payments_details(request):
    doctor = Doctor.objects.get(user=request.user)
    payments = base_model.Billing.objects.filter(appointment__doctor=doctor, status="Paid")
    context = {
        "payments":payments,
        "doctor":doctor
    }
    return render(request, "doctor/payments.html", context)

@login_required
def notifications(request):
    doctor = Doctor.objects.get(user=request.user)
    notifications = Notification.objects.filter(doctor=doctor, seen=False)
    context = {
        "notifications":notifications,
        "doctor":doctor
    }
    
    return render(request, "doctor/notifications.html", context)

@login_required
def mark_notification_seen(request, id):
    doctor = Doctor.objects.get(user=request.user)
    notifications = Notification.objects.get(doctor=doctor, id=id)
    notifications.seen = True
    notifications.save()
    
    messages.success(request, "Notification has been seen")
    return redirect("notifications")

@login_required
def edit_doctor_profile(request):
    doctor = Doctor.objects.get(user=request.user)
    formatted_next_available_appointment_date = doctor.next_available_appointement_date.strftime('%Y-%m-%d')
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        bio = request.POST.get("bio")
        country = request.POST.get("country")
        specialization = request.POST.get("specialization")
        qualifications = request.POST.get("qualifications")
        years_of_experience = request.POST.get("years_of_experience")
        next_available_appointment_date = request.POST.get("next_available_appointment_date")
        
        
        doctor.user.email = email
        doctor.full_name = full_name
        doctor.mobile = mobile
        doctor.bio = bio
        doctor.country = country
        doctor.specialization = specialization
        doctor.qualification = qualifications
        doctor.years_of_experience = years_of_experience
        doctor.next_available_appointement_date = next_available_appointment_date
        try:
            image = request.FILES["image"]
            doctor.profile_image = image
        except Exception:
            pass
        doctor.save()
        messages.success(request, "Profile has been successfully updated.")
        return redirect("dashboard")
    
    context = {
        "doctor":doctor,
        "formatted_next_available_appointment_date":formatted_next_available_appointment_date
    }
    return render(request, "doctor/edit-profile.html", context)