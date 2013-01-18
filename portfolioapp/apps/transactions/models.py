from django.db import models
from portfolioapp.apps.holdings.models import Holding

class Transaction(models.Model):
    holding = models.ForeignKey(Holding)
    quantity = models.DecimalField(default=0.0, decimal_places=5, max_digits=7)
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)