from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'registration-username', 'placeholder': 'Введите имя пользователя'})
        self.fields['password1'].widget.attrs.update({'id': 'registration-password1', 'placeholder': 'Введите пароль'})
        self.fields['password2'].widget.attrs.update({'id': 'registration-password2', 'placeholder': 'Повторите пароль'})

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'login-username', 'placeholder': 'Введите имя пользователя'})
        self.fields['password'].widget.attrs.update({'id': 'login-password', 'placeholder': 'Введите пароль'})