# markets/urls.py

from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.markets.views.stock_index', name='markets_stocks_index'),
    url(r'^(?P<stock_id>\d+)/$', 'portfolioapp.apps.markets.views.stock_show', name='markets_stocks_show'),
)