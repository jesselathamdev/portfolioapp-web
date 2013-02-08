from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # profiles (sign in, profile, etc)
    url(r'^sign-up/$', 'portfolioapp.apps.profiles.views.profile_create', name='profile_create'),
    url(r'^sign-in/$', 'django.contrib.auth.views.login', {'template_name': 'profiles/signin.html'}, name='profile_signin'),
    url(r'^sign-out/$', 'django.contrib.auth.views.logout', {'template_name': 'profiles/signout.html'}, name='profile_signout'),
    url(r'^profile/$', 'portfolioapp.apps.profiles.views.profile_edit', name='profile_edit'),

    # home page
    url(r'^$', 'portfolioapp.apps.home.views.index', name='home_index'),

    # transactions through portfolios
    url(r'^transactions/', 'portfolioapp.apps.portfolios.views.transaction_index_global', name='transaction_index_global'),

    # portfolios
    url(r'^portfolios/', include('portfolioapp.apps.portfolios.urls')),

    # admin
    url(r'^admin/', include('portfolioapp.apps.admin.urls')),

    # apis
    url(r'^api/markets/stocks/?', 'portfolioapp.apps.markets.views_api.stock_index', name='api_stock_index'),

    # helpers
    url(r'^dummy/?', 'portfolioapp.apps.core.views.dummy', name='dummy'),
)