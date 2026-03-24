from django.shortcuts import render, redirect
from django.http import HttpResponse
from hospitalsystem.models import Service
from django.contrib.auth.decorators import login_required
from .models import Appointement, Service, Billing
from doctors.models import Doctor
from doctors import models as doctor_model
from patients import models as patient_model
from patients.models import Patient
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import stripe
from django.http import JsonResponse
import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
from datetime import timezone
# You can then use timezone.utc




def home(request):
    services = Service.objects.all()
    context = {
        "services":services
    }
    return render(request, "userauth/index.html", context)

def service_detail(request, pk):
    service = Service.objects.get(id=pk)
    context = {
        "service":service
    }
    return render(request, "userauth/service_detail.html", context)

@login_required
def book_appointment(request, service_id, doctor_id):
    service = Service.objects.get(id=service_id)
    doctor = Doctor.objects.get(id=doctor_id)
    patient = Patient.objects.get(user=request.user)
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("dob")
        gender = request.POST.get("gender")
        
        #WE COLLECT THE USERNAME, EMAIL
        # all the information that are not in the appointment table
        #because we want to allow users to update
        #their bio data right in the booking form
        
        patient.full_name = full_name
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.date_of_birth = date_of_birth
        patient.user.email = email
        patient.save()
        
        #create appointment object
        appointment = Appointement.objects.create(service=service, issues=issues, symptoms=symptoms, doctor=doctor, patient=patient, 
        appointment_date=doctor.next_available_appointement_date)
        appointment.status = "scheduled"
        appointment.save()
        
        #create billing
        billing = Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = appointment.service.cost * 5 / 100
        billing.total = billing.sub_total + billing.tax
        billing.status = "Unpaid"
        billing.save()
        
        return redirect('checkout', billing.billing_id)
    
    context={
        "service":service,
        "doctor":doctor,
        "patient":patient
    }
    
    return render(request, "userauth/book_appointment.html", context)


@login_required
def checkout(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    
    context = {
        "billing":billing,
        "stripe_public_key":settings.STRIPE_PUBLIC_KEY,
        "paypal_client_id":settings.PAYPAL_CLIENT_ID
    }
    
    return render(request, "userauth/checkout.html", context)

@csrf_exempt
def stripe_payment(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    checkout_session = stripe.checkout.Session.create(
        customer_email=billing.patient.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'USD',
                    'product_data':{
                        'name':billing.patient.full_name
                    },
                    'unit_amount':int(billing.total * 100)
                },
                'quantity':1
                
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse("stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}"
    )
    
    return JsonResponse({"sessionId":checkout_session.id})


def stripe_payment_verify(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":
        if billing.status == "Unpaid":
            billing.status = "Paid"
            billing.save()
            billing.appointment.status = "scheduled"
            billing.appointment.save()
            
            doctor_model.Notification.objects.create(
                doctor=billing.appointment.doctor,
                appointment=billing.appointment,
                type="new appointment"
            )
            
            patient_model.Notification.objects.create(
                patient=billing.appointment.patient,
                appointment=billing.appointment,
                type="appointment scheduled"
            )
            
            merge_data = {
                "billing":billing
            }
            #send appointment email to doctor
            subject = "New appointment"
            text_body = render_to_string("email/new_appointment.txt", merge_data)
            html_body = render_to_string("email/new_appointment.html", merge_data)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[billing.appointment.doctor.user.email],
                body=text_body
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send(fail_silently=False)
            
            #send appointment booked email to patient
            subject = "Appointment Scheduled"
            text_body = render_to_string("email/appointment_booked.txt", merge_data)
            html_body = render_to_string("email/appointment_booked.html", merge_data)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[billing.appointment.patient.user.email],
                body=text_body
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send(fail_silently=False)
            
            
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
    else:
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")

def get_paypal_access_token():
    token_url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = {'grant_type':"client_credentials"}
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_ID)
    response = requests.post(token_url, data=data, auth=auth)
    
    if response.status_code == 200:
        print("Access Token:", response.json()['access_token'])
        return response.json()["access_token"]
    
    else:
        raise Exception(f"Failed to get access token from paypal. Status code:{response.status_code}")

def paypal_payment_verify(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    transaction_id = request.GET.get("transaction_id")
    paypal_api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{transaction_id}"
    headers = {
        'Content-Type':'application/json',
        "Authorization":f"Bearer {get_paypal_access_token()}"
    }
    response = requests.get(paypal_api_url, headers=headers)
    
    if response.status_code == 200:
        paypal_order_data = response.json()
        paypal_payment_status = paypal_order_data["status"]

        if paypal_payment_status == "COMPLETED":
            if billing.status == "Unpaid":
                billing.status = "Paid"
                billing.save()
                billing.appointment.status = "completed"
                billing.appointment.save()
                
                doctor_model.Notification.objects.create(
                    doctor=billing.appointment.doctor,
                    appointment=billing.appointment,
                    type="new appointment"
                )
                
                patient_model.Notification.objects.create(
                    patient=billing.appointment.patient,
                    appointment=billing.appointment,
                    type="appointment scheduled"
                )
                
                
                merge_data = {
                    "billing":billing
                }
                #send appointment email to doctor
                subject = "New appointment"
                text_body = render_to_string("email/new_appointment.txt", merge_data)
                html_body = render_to_string("email/new_appointment.html", merge_data)
                
                msg = EmailMultiAlternatives(
                    subject=subject,
                    from_email=settings.FROM_EMAIL,
                    to=[billing.appointment.doctor.user.email],
                    body=text_body
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send()
                
                #send appointment booked email to patient
                subject = "Appointment Scheduled"
                text_body = render_to_string("email/appointment_booked.txt", merge_data)
                html_body = render_to_string("email/appointment_booked.html", merge_data)
                
                msg = EmailMultiAlternatives(
                    subject=subject,
                    from_email=settings.FROM_EMAIL,
                    to=[billing.appointment.patient.user.email],
                    body=text_body
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send()
                
            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
        
    return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")
    
        
@login_required
def payment_status(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")
    
    context = {
        "payment_status":payment_status,
        "billing":billing
    }
    
    return render(request, "userauth/payment_status.html", context)



