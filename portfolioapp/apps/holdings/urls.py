from django.conf.urls import patterns, url

from portfolioapp.apps.holdings import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='holding_index'),
)