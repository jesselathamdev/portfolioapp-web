from django.conf.urls import patterns, url
from portfolios import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<portfolio_id>\d+)/?', views.detail, name='detail'),
)