from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

def index(request):
    return render(request, 'home/index.html', {'user': request.user})