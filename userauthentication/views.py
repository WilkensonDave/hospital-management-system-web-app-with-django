from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from userauthentication.forms import UserRegisterForm, UserLoginForm
from userauthentication.models import User
from django.contrib.auth import authenticate, login, logout
from doctors.models import Doctor
from patients.models import Patient
# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get("email")
            full_name = form.cleaned_data.get("full_name")
            password1 = form.cleaned_data.get("password1")
            user_type = form.cleaned_data.get("user_type")
            
            user = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request, user)
                
                if user_type == "doctor":
                    Doctor.objects.create(user=user, full_name=full_name)
                    
                else:
                    Patient.objects.create(user=user, full_name=full_name)
                    
                messages.success(request, "You have been successfully registered")
                return redirect("/")
            
            else:
                messages.error(request, "Authentication Failed, please try again!")
                return redirect("register-user")
        else:
            messages.error(request, "Invalid data")
            return redirect("register-user")
            
    else:
        form = UserRegisterForm()
        context = {
            "form":form
        }
        return render(request, "userauth/register.html", context)

def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password1")
            
            user = authenticate(request, email=email, password=password1)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You have been successfully logged in.")
                next_url = request.GET.get("next", "/")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid email or password")
        
    form = UserLoginForm()
    context = {
        "form":form
    }
    return render(request, "userauth/login.html", context)

def logout_view(request):
    logout(request)
    next_url = request.GET.get("next")
    messages.success(request, "You have logged out.")
    if next_url:
        return redirect(next_url)
    return redirect("login")