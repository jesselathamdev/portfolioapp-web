# admin/forms.py
from django import forms

from portfolioapp.apps.markets.models import Stock

class StockEditForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('name', 'symbol', 'last_price',)


class StockSearchForm(forms.ModelForm):
    search = forms.CharField(max_length=50)