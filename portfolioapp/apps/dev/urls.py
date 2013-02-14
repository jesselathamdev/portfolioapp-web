# admin/urls.py
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.dev.views.sample1_index', name='dev_sample1_index'),
)