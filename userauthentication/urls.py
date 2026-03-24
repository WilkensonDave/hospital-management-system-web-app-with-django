from django.urls import path
from . import views


urlpatterns = [
    path("sign-up/", views.register_view, name="register-user"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]
