from django.conf.urls import patterns, include, url

from .views import portfolio_index, portfolio_detail, holding_index, transaction_index, holding_create

urlpatterns = patterns('',
    url(r'^$', portfolio_index, name='portfolio_index'),
    url(r'^(?P<portfolio_id>\d+)/$', portfolio_detail, name='portfolio_detail'),
    url(r'^(?P<portfolio_id>\d+)/holdings/$', holding_index, name='holding_index'),
    url(r'^(?P<portfolio_id>\d+)/holdings/add/$', holding_create, name='holding_create'),
    url(r'^(?P<portfolio_id>\d+)/holdings/(?P<holding_id>\d+)/transactions/$', transaction_index, name='transaction_index'),
)