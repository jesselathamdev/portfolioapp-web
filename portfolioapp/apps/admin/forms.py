# admin/forms.py

from django import forms

from portfolioapp.apps.markets.models import Stock
from portfolioapp.apps.api.models import ApiToken


class StockEditForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('name', 'symbol', 'last_price',)


class StockSearchForm(forms.Form):
    search_term = forms.CharField(max_length=50)


class ApiTokenDeleteForm(forms.Form):
    class Meta:
        model = ApiToken