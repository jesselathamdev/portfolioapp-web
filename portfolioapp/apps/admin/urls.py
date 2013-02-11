# admin/urls.py
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.admin.views.home_index', name='admin_home_index'),
    url(r'^stocks/$', 'portfolioapp.apps.admin.views.stock_index', name='admin_stock_index'),
    url(r'^stocks2/$', 'portfolioapp.apps.admin.views.stock_index2', name='admin_stock_index2'),
    url(r'^stocks3/$', 'portfolioapp.apps.admin.views.stock_index3', name='admin_stock_index3'),
)