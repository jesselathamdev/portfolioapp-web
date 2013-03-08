# portfolios/forms.py
from django import forms

from .models import Portfolio, Holding

class CreatePortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name', 'user',)


class CreateHoldingForm(forms.ModelForm):
    stock_name = forms.CharField(max_length=250)

    class Meta:
        model = Holding
        fields = ('stock', 'portfolio',)