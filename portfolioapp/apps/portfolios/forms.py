# portfolios/forms.py

from django import forms

from .models import Portfolio, Holding, Transaction


class CreatePortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name', 'user',)


class CreateHoldingForm(forms.ModelForm):
    stock_name = forms.CharField(max_length=250)

    class Meta:
        model = Holding
        fields = ('stock', 'portfolio',)


class CreateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('date_transacted', 'type', 'quantity', 'value', 'comment', 'commission', 'holding',)