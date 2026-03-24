from django.urls import path
from . import views

urlpatterns = [
    path("dashboard", views.patients_dashboard, name="patients-dashboard"),
    path("patient_appointments/", views.appointments, name="patient_appointments"),
    path("appointment-details/<appointment_id>/", views.appointment_details_patients, name="appointment_details_patients"),
    path("cancel_appointment/<appointment_id>/", views.cancel_appointment, name="cancel_appointment"),
    path("activate_appointmentt/<appointment_id>/", views.activate_appointment, name="activate_appointment"),
    path("patients_notifications/", views.patient_notifications, name="patient_notifications"),
    path("patient_payments/", views.payments_details, name="patient_payments"),
    path("patient_notification_seen/<id>/", views.patient_notification_seen, name="patient_notification_seen"),
    path("patient_profile/", views.edit_patient_profile, name="edit_patient_profile"),
    path("about/", views.about_us, name="about"),
    path("contact/", views.contact_us, name="contact"),
    path("medical_reports/", views.medical_reports, name="medical_reports"),
    path("lab_tests/", views.lab_tests, name="lab_tests"),
    path("prescriptions/", views.patient_prescription, name="patient_prescription")
]
