from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("appointments/", views.appointments, name="appointments"),
    path("appointment-details/<appointment_id>/", views.appointment_details, name="appointment_details"),
    path("cancel_appointment/<appointment_id>/", views.cancel_appointment, name="cancel-appointment"),
    path("activate_appointment/<appointment_id>/", views.activate_appointment, name="activate-appointment"),
    path("complete_appointment/<appointment_id>/", views.complete_appointment, name="complete-appointment"),
    path("edit_medical_report/<appointment_id>/<medical_report_id>/", views.edit_medical_report, name="edit-medical-report"),
    path("add_medical_report/<appointment_id>/", views.add_medical_report, name="add-medical-report"),
    path("add_lab_test_report/<appointment_id>/", views.add_lab_test_report, name="add-lab-test-report"),
    path("edit_lab_test_report/<appointment_id>/<lab_test_id>/", views.edit_lab_test_report, name="edit-lab-test-report"),
    path("edit_prescription/<appointment_id>/<prescription_id>/", views.edit_prescription, name="edit-prescription"),
    path("add_prescription/<appointment_id>/", views.add_prescription, name="add-prescription"),
    path("payments_details/", views.payments_details, name="payments_details"),
    path("notifications/", views.notifications, name="notifications"),
    path("mark_notification_seen/<id>", views.mark_notification_seen, name="mark-notification-seen"),
    path("edit-doctor-profile/", views.edit_doctor_profile, name="edit_doctor_profile"),
]
  