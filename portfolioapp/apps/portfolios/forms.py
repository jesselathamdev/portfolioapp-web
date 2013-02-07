# portfolios/forms.py
from django import forms

from .models import Holding

class CreateHolding(forms.ModelForm):
    class Meta:
        model = Holding
        fields = ('stock', 'portfolio',)