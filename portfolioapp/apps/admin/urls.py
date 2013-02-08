# admin/urls.py
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.admin.views.home_index', name='admin_home_index'),
    url(r'^stocks/$', 'portfolioapp.apps.admin.views.stock_index', name='admin_stock_index'),
)