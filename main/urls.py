from django.urls import path
from main.views import IndexView, RegistrationView, LoginView, LogoutView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
