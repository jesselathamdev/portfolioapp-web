# portfolios/models.py
import datetime

from django.conf import settings
from django.db import models

from .managers import PortfolioManager, HoldingManager

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    objects = PortfolioManager()


class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio)
    market = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name + " (" + self.market + ":" + self.symbol + ")"

    def market_symbol(self):
        return "%s:%s" % (self.market, self.symbol)

    objects = HoldingManager()


class Transaction(models.Model):
    SHARES_IN = 0
    SHARES_OUT = 1
    BUY = 5
    SELL = 6

    TYPE_CHOICES = (
        (BUY, "Buy"),
        (SELL, "Sell"),
        (SHARES_IN, "Shares in"),
        (SHARES_OUT, "Shares out"),
    )

    holding = models.ForeignKey(Holding)
    quantity = models.DecimalField(default=0.0, decimal_places=5, max_digits=10)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=5)
    date_transacted = models.DateTimeField(default=datetime.datetime.now)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s %s on %s' % (self.get_type_display(), self.quantity, self.date_created.strftime("%M/%d/%y"))
        # return u"%s (%s)" % (self.holding.name, self.quantity) #risky, queries for each name of parent
