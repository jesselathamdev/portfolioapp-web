# markets/models.py

from datetime import datetime

from django.db import models

from portfolioapp.apps.core.mixins import TimeStampMixin

class Market(TimeStampMixin, models.Model):
    name = models.CharField(max_length=250, blank=False) # ex: Toronto Stock Exchance, NASDAQ
    mic = models.CharField(max_length=5, unique=True, blank=False) # ex: XTSE, XNAS
    acr = models.CharField(max_length=20, blank=True) # ex: TSX, NASDAQ
    country = models.CharField(max_length=50, blank=False)
    country_code = models.CharField(max_length=2, blank=False)
    city = models.CharField(max_length=30, blank=False)
    website = models.CharField(max_length=250, blank=True)
    active = models.BooleanField(blank=False, default=True)


class Stock(TimeStampMixin, models.Model):
    name = models.CharField(max_length=250, blank=False) # ex: BlackBerry Inc., Microsoft Inc.
    symbol = models.CharField(max_length=8, blank=False) # ex: BB:TSX, MSFT:NASDAQ
    last_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    date_last_price_updated = models.DateTimeField(default=datetime.now())
    market = models.ForeignKey(Market)

    def __unicode__(self):
        return '%s:%s' % (self.name, self.symbol)
