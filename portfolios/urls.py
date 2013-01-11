from django.conf.urls import patterns, url
from portfolios import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)