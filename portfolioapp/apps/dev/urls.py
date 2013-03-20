# admin/urls.py

from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.dev.views.sample1_index', name='dev_sample1_index'),
    url(r'^api-console/$', 'portfolioapp.apps.dev.views.api_console_index', name='dev_api_console_index'),
)