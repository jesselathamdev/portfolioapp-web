# portfolios/models.py
from django.db import models
from portfolioapp.apps.core.models import User

class Portfolio(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio)
    market = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name + " (" + self.market + ":" + self.symbol + ")"


class Transaction(models.Model):
    holding = models.ForeignKey(Holding)
    quantity = models.DecimalField(default=0.0, decimal_places=5, max_digits=7)
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)