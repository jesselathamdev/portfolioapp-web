# urls.py

from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
    # site and generial static pages
    url(r'^$', include('portfolioapp.apps.site.urls')),

    # profiles (sign in, profile, etc)
    url(r'^sign-up/$', 'portfolioapp.apps.profiles.views.profile_create', name='profile_create'),
    url(r'^sign-in/$', 'portfolioapp.apps.profiles.views.login', name='profile_signin'),
    url(r'^sign-out/$', 'django.contrib.auth.views.logout', {'template_name': 'profiles/signout.html'}, name='profile_signout'),
    url(r'^profile/$', 'portfolioapp.apps.profiles.views.profile_edit', name='profile_edit'),

    # stocks (markets)
    url(r'^stocks/', include('portfolioapp.apps.markets.urls')),

    # portfolios
    url(r'^portfolios/', include('portfolioapp.apps.portfolios.urls')),

    # activity
    url(r'^activity/$', 'portfolioapp.apps.portfolios.views.activity_index', name='activity_index'),

    # custom admin
    url(r'^admin/', include('portfolioapp.apps.admin.urls')),

    # apis (internal)
    url(r'^api/markets/stocks2/?', 'portfolioapp.apps.markets.views_api.stock_index2', name='api_stock_index2'),
    url(r'^api/markets/stocks/?', 'portfolioapp.apps.markets.views_api.stock_index', name='api_stock_index'),

    # apis (external)
    url(r'^api/v2/', include('portfolioapp.apps.api.v2_urls')),
)

# only available in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^dev/', include('portfolioapp.apps.dev.urls')),
    )

# only available in non-debug mode (i.e. production)
if not settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )