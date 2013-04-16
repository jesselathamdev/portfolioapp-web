# api/v2_urls.py
from django.conf.urls import patterns, url
from .v2_api import get_portfolios, get_activity, get_markets, token_create

urlpatterns = patterns('',
    url(r'^portfolios/', get_portfolios),
    url(r'^activity/', get_activity),
    url(r'^markets/', get_markets),
    url(r'^auth/token/create', token_create),
)