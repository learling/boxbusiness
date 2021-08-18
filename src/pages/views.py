from django.shortcuts import render
from django.conf import settings


def home(request):
    return render(request, 'pages/home.html', {})

def impressum(request):
    return render(request, 'pages/impressum.html', settings.SITE_OWNER)

def datenschutz(request):
    return render(request, 'pages/datenschutz.html', {})