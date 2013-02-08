from django.conf.urls import patterns, url

from .views import portfolio_index, portfolio_detail, holding_index, transaction_index, holding_create

urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.portfolios.views.portfolio_index', name='portfolio_index'),
    url(r'^(?P<portfolio_id>\d+)/$', 'portfolioapp.apps.portfolios.views.portfolio_detail', name='portfolio_detail'),
    url(r'^(?P<portfolio_id>\d+)/holdings/$', 'portfolioapp.apps.portfolios.views.holding_index', name='holding_index'),
    url(r'^(?P<portfolio_id>\d+)/holdings/add/?', 'portfolioapp.apps.portfolios.views.holding_create', name='holding_create'),
    url(r'^(?P<portfolio_id>\d+)/holdings/(?P<holding_id>\d+)/transactions/$', 'portfolioapp.apps.portfolios.views.transaction_index', name='transaction_index'),
)