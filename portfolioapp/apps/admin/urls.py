# admin/urls.py
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.admin.views.home_index', name='admin_home_index'),
    url(r'^stocks/$', 'portfolioapp.apps.admin.views.stock_index', name='admin_stock_index'),
    url(r'^stocks-endless-pagination/$', 'portfolioapp.apps.admin.views.ep_stock_index', name='admin_stock_index_ep'),
    url(r'^stocks-dajax/$', 'portfolioapp.apps.admin.views.dajax_stock_index', name='admin_stock_index_dajax'),
)