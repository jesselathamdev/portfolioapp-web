# portfolios/forms.py
from django import forms

from .models import Portfolio, Holding

class CreatePortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name', 'user',)


class CreateHoldingForm(forms.ModelForm):
    class Meta:
        model = Holding
        fields = ('stock', 'portfolio',)