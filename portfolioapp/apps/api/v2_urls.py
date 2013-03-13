# api/v2_urls.py
from django.conf.urls import patterns, url
from .v2_api import get_portfolios

urlpatterns = patterns('',
    url(r'^portfolios/', 'portfolioapp.apps.portfolios.views.portfolio_index', name='portfolio_index'),
    url(r'^add/$', 'portfolioapp.apps.portfolios.views.portfolio_create', name='portfolio_create'),
    url(r'^(?P<portfolio_id>\d+)/delete/$', 'portfolioapp.apps.portfolios.views.portfolio_delete', name='portfolio_delete'),
)