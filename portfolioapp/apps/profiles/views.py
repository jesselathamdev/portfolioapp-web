# profiles/views.py

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib import messages

from .forms import LoginForm, CreateUserProfileForm, EditUserProfileForm


def login(request):
    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)

            if user is not None:
                if user.is_active:
                    if not request.POST.get('remember_me', False):
                        request.session.set_expiry(0)
                    django_login(request, user)

                    return HttpResponseRedirect(reverse('site_index')) # success

            else:
                form.errors['login'] = 'The email and/or password provided was invalid.'

                return render(request, 'profiles/signin.html', {'form': form})

        else:
            form.errors['login'] = 'The email and/or password provided was invalid.'

            return render(request, 'profiles/signin.html', {'form': form})

    else:
        logout(request)
        form = LoginForm()

        return render(request, 'profiles/signin.html', {'form': form})


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
                    django_login(request, user)
                    return HttpResponseRedirect(reverse('site_index'))
        else:
            return render(request, 'profiles/signup.html', {'form': form})

    else:
        form = CreateUserProfileForm()
        return render(request, 'profiles/signup.html', {'form': form})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('site_index'))

        form = EditUserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile saved successfully.')

            return HttpResponseRedirect(reverse('profile_edit'))
    else:
        form = EditUserProfileForm(instance=request.user)

        return render(request, 'profiles/edit.html', {'form': form})
