# api/v2_urls.py
from django.conf.urls import patterns, url
from .v2_api import get_portfolios

urlpatterns = patterns('',
    url(r'^portfolios/', get_portfolios),
)