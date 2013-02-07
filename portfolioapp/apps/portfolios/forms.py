# portfolios/forms.py
from django import forms

from .models import Holding

class CreateHolding(forms.ModelForm):
    stock_id = forms.CharField(max_length=100)

    class Meta:
        model = Holding
        fields = ('stock_id',)



