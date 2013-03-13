# api/v2_urls.py
from django.conf.urls import patterns, url
from .v2_api import get_portfolios, get_markets

urlpatterns = patterns('',
    url(r'^portfolios/', get_portfolios),
    url(r'^markets/', get_markets),
)