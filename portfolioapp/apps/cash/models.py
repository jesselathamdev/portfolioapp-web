# cash/models.py

import datetime

from django.db import models
from django.conf import settings

from portfolioapp.apps.core.mixins import TimeStampMixin

from portfolioapp.apps.portfolios.models import Portfolio
from .managers import CashManager

class Cash(TimeStampMixin, models.Model):
    DEPOSIT = 0
    WITHDRAWL = 1

    TYPE_CHOICES = (
        (DEPOSIT, 'Deposit'),
        (WITHDRAWL, 'Withdrawal')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    portfolio = models.ForeignKey(Portfolio)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, null=True)
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=9)
    comment = models.CharField(max_length=250, default='', blank=True, null=True)
    date_transacted = models.DateTimeField(default=datetime.datetime.now)

    objects = CashManager()

    def __unicode__(self):
        return '%s of %s on %s' % (self.get_type_display(), abs(self.amount), self.date_transacted.strftime("%m/%d/%Y"))