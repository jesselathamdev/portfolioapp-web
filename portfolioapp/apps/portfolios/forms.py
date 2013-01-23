# portfolios/forms.py
from django.forms import ModelForm
from .models import Holding

class CreateHolding(ModelForm):
    class Meta:
        model = Holding
        fields = ('market', 'symbol', 'name')
