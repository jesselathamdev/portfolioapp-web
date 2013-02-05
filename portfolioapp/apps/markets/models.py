# markets/models.py

from django.db import models

from portfolioapp.apps.core.mixins import TimeStampMixin

class Market(TimeStampMixin, models.Model):
    name = models.CharField(max_length=250, blank=False)
    mic = models.CharField(max_length=5, unique=True, blank=False)
    acr = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=False)
    country_code = models.CharField(max_length=2, blank=False)
    city = models.CharField(max_length=30, blank=False)
    website = models.CharField(max_length=250, blank=True)
    active = models.BooleanField(blank=False, default=True)