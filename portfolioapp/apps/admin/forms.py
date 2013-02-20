# admin/forms.py
from django import forms

from portfolioapp.apps.markets.models import Stock

class EditStockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('name', 'symbol', 'last_price',)