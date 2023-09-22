from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm


def registration_modal_form(request):
    return {"registration_form": RegistrationForm()}


def authentication_modal_form(request):
    return {"authentication_form": AuthenticationForm()}
