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
    comment = models.CharField(max_length=250, default='', blank=True, null=True)
    commission = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    date_transacted = models.DateTimeField(default=datetime.datetime.now)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s %s on %s' % (self.get_type_display(), self.quantity, self.date_created.strftime("%M/%d/%y"))
        # return u"%s (%s)" % (self.holding.name, self.quantity) #risky, queries for each name of parent

    def save(self, *args, **kwargs):
        # change the sign of the quantity being saved depending on the type of transaction
        if (self.type == self.SHARES_OUT or self.type == self.SELL) and self.quantity >= 0:
            self.quantity *= -1
        elif (self.type == self.SHARES_IN or self.type == self.BUY) and self.quantity <= 0:
            self.quantity *= -1
        super(Transaction, self).save(*args, **kwargs)