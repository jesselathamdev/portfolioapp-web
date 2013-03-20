# api/forms.py

from django import forms


class AuthForm(forms.Form):
    email = forms.EmailField(max_length=75, required=True)
    password = forms.CharField(max_length=75, required=True)
    identifier = forms.CharField(max_length=50, required=True)

