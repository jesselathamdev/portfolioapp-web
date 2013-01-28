# portfolios/models.py
from django.conf import settings
from django.db import models

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
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

    def market_symbol(self):
        return "%s:%s" % (self.market, self.symbol)


class Transaction(models.Model):
    SHARES_IN = 0
    SHARES_OUT = 1
    BUY = 5
    SELL = 6

    CATEGORY_CHOICES = (
        (SHARES_IN, "Shares in"),
        (SHARES_OUT, "Shares out"),
        (BUY, "Buy"),
        (SELL, "Sell"),
    )

    holding = models.ForeignKey(Holding)
    quantity = models.DecimalField(default=0.0, decimal_places=5, max_digits=7)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    category_id = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES, default=5)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.date_created.strftime("%M/%d/%y")
        # return u"%s (%s)" % (self.holding.name, self.quantity) #risky, queries for each name of parent
