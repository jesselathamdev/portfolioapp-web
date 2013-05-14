# api/v2_urls.py

from django.conf.urls import patterns, url
from .v2_api import get_portfolios, get_portfolio_holdings, get_holdings, get_activity, get_markets, token_create, token_delete


urlpatterns = patterns('',
    url(r'^portfolios/(?P<portfolio_id>\d+)/holdings', get_portfolio_holdings),
    url(r'^portfolios/', get_portfolios),
    url(r'^activity/', get_activity),
    url(r'^markets/', get_markets),
    url(r'^auth/token/create', token_create),
    url(r'^auth/token/(?P<token>[a-zA-Z0-9]{30,})/delete', token_delete),
)