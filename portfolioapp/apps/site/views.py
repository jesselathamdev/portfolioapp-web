# site/views.py

from django.shortcuts import render


def home_index(request):
    return render(request, 'site/home_index.html')