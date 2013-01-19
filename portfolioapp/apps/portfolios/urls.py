from django.conf.urls import patterns, include, url

from portfolioapp.apps.portfolios import views

urlpatterns = patterns('',
    url(r'^$', views.portfolio_index, name='portfolio_index'),
    url(r'^(?P<portfolio_id>\d+)/$', views.portfolio_detail, name='portfolio_detail'),
    url(r'^(?P<portfolio_id>\d+)/holdings/', views.holding_index, name='holding_index'),
)