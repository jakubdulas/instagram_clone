from django.shortcuts import render
from .models import *
# Create your views here.

def home(request):
    

    context = {}
    return render(request, 'home.html', context)

def profile(request):
    return render(request, 'profile.html')


def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')