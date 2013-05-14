# admin/urls.py
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.admin.views.home_index', name='admin_home_index'),

    url(r'^stocks/$', 'portfolioapp.apps.admin.views.stock_index', name='admin_stock_index'),
    url(r'^stocks/(?P<stock_id>\d+)/$', 'portfolioapp.apps.admin.views.stock_edit', name='admin_stock_edit'),

    url(r'^markets/$', 'portfolioapp.apps.admin.views.market_index', name='admin_market_index'),

    url(r'^users/$', 'portfolioapp.apps.admin.views.profile_index', name='admin_profile_index'),
    url(r'^users/(?P<user_id>\d+)/$', 'portfolioapp.apps.admin.views.profile_edit', name='admin_profile_edit'),

    url(r'^api/$', 'portfolioapp.apps.admin.views.api_log_index', name='admin_api_log_index'),
    url(r'^api/(?P<api_log_id>\d+)/$', 'portfolioapp.apps.admin.views.api_log_show', name='admin_api_log_show'),

    url(r'^api-tokens/$', 'portfolioapp.apps.admin.views.api_token_index', name='admin_api_token_index'),
    url(r'^api-tokens/(?P<api_token_id>\d+)/$', 'portfolioapp.apps.admin.views.api_token_show', name='admin_api_token_show'),
)