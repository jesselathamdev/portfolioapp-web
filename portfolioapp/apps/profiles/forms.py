# profiles/forms.py
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .models import User

class EditUserProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')

class AdminEditUserProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_admin')


class CreateUserProfileForm(ModelForm):
    """A form for creating new users. Includes all the
       required fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CreateUserProfileForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CreateUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = ''
        self.fields['password1'].initial = ''
        self.fields['password2'].initial = ''
        self.fields['first_name'].initial = ''
        self.fields['last_name'].initial = ''


class LoginForm(ModelForm):
    username = forms.CharField(max_length=75)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')