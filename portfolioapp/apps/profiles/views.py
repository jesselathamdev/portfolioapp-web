# profiles/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .forms import EditUserProfile

def profile_edit(request):
    form = EditUserProfile(instance=request.user)
    return render(request, 'profiles/edit.html', {'form': form})
