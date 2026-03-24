from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("service-detail/<int:pk>/", views.service_detail, name="service-detail"),
    path("book-appointment/<service_id>/<doctor_id>", views.book_appointment, name="book-appointment"),
    path("checkout/<billing_id>/", views.checkout, name="checkout"),
    path("payment_status/<billing_id>/", views.payment_status, name="payment_status"),
    path("stripe_payment/<billing_id>/", views.stripe_payment, name="stripe_payment"),
    path("stripe_payment_verify/<billing_id>/", views.stripe_payment_verify, name="stripe_payment_verify"),
    path("stripe_payment_verify/<billing_id>/", views.paypal_payment_verify, name="paypal_payment_verify"),
]
