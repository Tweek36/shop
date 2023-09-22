from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .forms import RegistrationForm
from django.views import View
from django.contrib.auth.forms import AuthenticationForm


class IndexView(View):
    def get(self, request):
        products = (
            ("CPU", "cpu"),
            ("Cooler", "cooler"),
            ("HDD", "hdd"),
            ("Motherboard", "motherboard"),
            ("Power supply", "power_supply"),
            ("RAM", "ram"),
            ("SSD", "ssd"),
            ("Video card", "video_card"),
        )
        return render(request, "main/index.html", {"products": products})


class LoginView(View):
    def post(self, request):
        login_form = AuthenticationForm(request, data=request.POST)
        if not login_form.is_valid():
            return JsonResponse({"err": "Invalid form data!"}, status=401)
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Вход выполнен успешно"})
        else:
            return JsonResponse(
                {"err": "Неверное имя пользователя или пароль"}, status=401
            )


class LogoutView(View):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"message": "Выход выполнен успешно"})
        else:
            return JsonResponse({"err": "Вы не вошли в систему"}, status=401)


class RegistrationView(View):
    def post(self, request):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"err": "Invalid form data!"}, status=401)
        user = form.save()
        login(request, user)
