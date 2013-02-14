# dev/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from portfolioapp.apps.core.decorators import is_admin

@user_passes_test(is_admin)
def sample1_index(request):
    return render(request, 'dev/sample1.html', {})