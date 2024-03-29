# portfolios/models.py

import datetime

from django.conf import settings
from django.db import models

from portfolioapp.apps.markets.models import Stock
from portfolioapp.apps.core.mixins import TimeStampMixin

class Portfolio(TimeStampMixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'portfolios'

    def __unicode__(self):
        return self.name


class PortfolioDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    holding_count = models.IntegerField()
    book_value = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    market_value = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    net_gain_dollar = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    net_gain_percent = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)

    class Meta:
        db_table = 'portfolio_details'
        managed = False

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.holding_count)


class PortfolioHolding(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    stock_name = models.CharField(max_length=200)
    stock_symbol = models.CharField(max_length=10)
    market_code = models.CharField(max_length=10)
    last_price = models.DecimalField(decimal_places=2, max_digits=7)
    date_last_price_updated = models.DateTimeField()
    total_quantity = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    avg_cost = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    max_cost = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    min_cost = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    book_value = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    market_value = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    net_gain_dollar = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    net_gain_percent = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)
    portfolio_makeup_percent = models.DecimalField(default=0.0, decimal_places=5, max_digits=13)

    class Meta:
        db_table = 'portfolio_holdings'
        managed = False

    def __unicode__(self):
        return '%s' % (self.portfolio.name)


class Holding(TimeStampMixin, models.Model):
    portfolio = models.ForeignKey(Portfolio)
    stock = models.ForeignKey(Stock, default=1)

    class Meta:
        db_table = 'holdings'

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return '%s (%s:%s)' % (self.stock.name, self.stock.symbol, self.stock.market.acr)


class Transaction(TimeStampMixin, models.Model):
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
    value = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=5)
    comment = models.CharField(max_length=250, default='', blank=True, null=True)
    commission = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    date_transacted = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'transactions'

    def __unicode__(self):
        return '%s %s on %s' % (self.get_type_display(), self.quantity, self.date_created.strftime("%m/%d/%Y"))

    def save(self, *args, **kwargs):
        # change the sign of the quantity being saved depending on the type of transaction
        if (self.type == self.SHARES_OUT or self.type == self.SELL) and self.quantity >= 0:
            self.quantity *= -1
        elif (self.type == self.SHARES_IN or self.type == self.BUY) and self.quantity <= 0:
            self.quantity *= -1
        super(Transaction, self).save(*args, **kwargs)


class Activity(models.Model):
    SHARES_IN = 0
    SHARES_OUT = 1
    BUY = 5
    SELL = 6
    DEPOSIT = 10
    WITHDRAWAL = 11

    TYPE_CHOICES = (
        (BUY, "Buy"),
        (SELL, "Sell"),
        (SHARES_IN, "Shares in"),
        (SHARES_OUT, "Shares out"),
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal')
    )

    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    date_transacted = models.DateTimeField()
    name = models.CharField(max_length=250)
    symbol = models.CharField(max_length=10)
    acr = models.CharField(max_length=10)
    quantity = models.DecimalField(decimal_places=2, max_digits=6)
    value = models.DecimalField(decimal_places=2, max_digits=7)
    commission = models.DecimalField(decimal_places=2, max_digits=6)
    comment = models.CharField(max_length=250)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING)
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'activity'
        managed = False

    def __unicode__(self):
        return '%s %s on %s' % (self.get_type_display(), self.quantity, self.date_transacted.strftime("%m/%d/%Y"))

    def full_name(self):
        if self.symbol == '' and self.acr == '':
            return self.name
        else:
            return '%s (%s:%s)' % (self.name, self.symbol, self.acr)