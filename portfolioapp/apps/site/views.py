# site/views.py

from django.shortcuts import render


def site_index(request):
    return render(request, 'site/site_index.html')