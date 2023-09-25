from main.forms import RegistrationForm, LoginForm


def registration_form(request):
    return {"registration_form": RegistrationForm()}


def authentication_form(request):
    return {"authentication_form": LoginForm()}
