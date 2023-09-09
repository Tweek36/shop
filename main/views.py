from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from .models import Product
from django.contrib.auth import login

def index(request):
    if request.method == 'POST':
        print(f'--->{request.POST}')
        login = AuthenticationForm(data=request.POST)
        if login.is_valid():
            user = login.get_user()
            login(request, user)
    else:
        login = AuthenticationForm()
    return render(request, 'main/index.html', {'login': login})

