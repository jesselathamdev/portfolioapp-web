# profiles/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .forms import CreateUserProfileForm, EditUserProfileForm

def profile_create(request):
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('home_index'))

        form = CreateUserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('portfolio_index'))
        else:
            return render(request, 'profiles/create.html', {'form': form})

    else:
        form = CreateUserProfileForm()
        return render(request, 'profiles/create.html', {'form': form})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('home_index'))

        form = EditUserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile_edit'))
    else:
        form = EditUserProfileForm(instance=request.user)
        return render(request, 'profiles/edit.html', {'form': form})
