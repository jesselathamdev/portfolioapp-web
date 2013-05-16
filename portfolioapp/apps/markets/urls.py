# admin/urls.py
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.markets.views.stock_index', name='market_stock_index'),
    # url(r'^stocks/(?P<stock_id>\d+)/$', 'portfolioapp.apps.markets.views.stock_edit', name='market_stock_show'),
)