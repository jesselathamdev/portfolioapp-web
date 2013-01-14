from django.conf.urls import patterns, include, url

from portfolios import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='portfolio_index'),
    url(r'^(?P<portfolio_id>\d+)/$', views.detail, name='portfolio_detail'),
    url(r'^(?P<portfolio_id>\d+)/holdings/', include('holdings.urls', namespace="holdings")),
)