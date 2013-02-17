from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # profiles (sign in, profile, etc)
    url(r'^sign-up/$', 'portfolioapp.apps.profiles.views.profile_create', name='profile_create'),
    url(r'^sign-in/$', 'django.contrib.auth.views.login', {'template_name': 'profiles/signin.html'}, name='profile_signin'),
    url(r'^sign-out/$', 'django.contrib.auth.views.logout', {'template_name': 'profiles/signout.html'}, name='profile_signout'),
    url(r'^profile/$', 'portfolioapp.apps.profiles.views.profile_edit', name='profile_edit'),

    # home page
    url(r'^$', 'portfolioapp.apps.home.views.index', name='home_index'),

    # portfolios
    url(r'^portfolios/', include('portfolioapp.apps.portfolios.urls')),

    # transactions through portfolios
    url(r'^transactions/', 'portfolioapp.apps.portfolios.views.transaction_global_index', name='transaction_global_index'),

    # custom admin
    url(r'^admin/', include('portfolioapp.apps.admin.urls')),

    # apis
    url(r'^api/markets/stocks/?', 'portfolioapp.apps.markets.views_api.stock_index', name='api_stock_index'),

    # dev helpers
    url(r'^dummy/?', 'portfolioapp.apps.core.views.dummy', name='dummy'),
    url(r'^dev/', include('portfolioapp.apps.dev.urls')),

    # dajaxice
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    # urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )