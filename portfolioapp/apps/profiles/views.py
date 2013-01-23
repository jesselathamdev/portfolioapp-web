# profiles/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .forms import EditUserProfile

@login_required
def profile_edit(request):
    if request.method == "POST":
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('home_index'))

        form = EditUserProfile(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile_edit'))
    else:
        form = EditUserProfile(instance=request.user)
        return render(request, 'profiles/edit.html', {'form': form})
