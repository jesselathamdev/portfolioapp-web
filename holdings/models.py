from django.db import models

from portfolios.models import Portfolio

class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio)
    market = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name + " (" + self.market + ":" + self.symbol + ")"