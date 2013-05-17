# markets/forms.py

from django import forms

from .models import Stock


class StockSearchForm(forms.Form):
    search_term = forms.CharField(max_length=200, required=False)
    stock_id = forms.IntegerField(required=False)