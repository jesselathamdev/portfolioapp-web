from django.conf.urls import patterns, include, url
from django.contrib import admin

from portfolioapp.apps.home import views

admin.autodiscover()

urlpatterns = patterns('',
    # profiles (sign in, profile, etc)
    url(r'^sign-up/$', 'portfolioapp.apps.profiles.views.profile_create', name='profile_create'),
    url(r'^sign-in/$', 'django.contrib.auth.views.login', {'template_name': 'profiles/signin.html'}, name='profile_signin'),
    url(r'^sign-out/$', 'django.contrib.auth.views.logout', {'template_name': 'profiles/signout.html'}, name='profile_signout'),
    url(r'^profile/$', 'portfolioapp.apps.profiles.views.profile_edit', name='profile_edit'),

    # home page
    url(r'^$', views.index, name="home_index"),

    # transactions through portfolios
    url(r'^transactions/', 'portfolioapp.apps.portfolios.views.transaction_list_index', name='transaction_list_index'),

    # portfolios
    url(r'^portfolios/', include('portfolioapp.apps.portfolios.urls')),

    # apis
    url(r'^api/markets/stocks/$', 'portfolioapp.apps.markets.views_api.stock_index', name='api_stock_index'),

    # django admin
    url(r'^admin/', include(admin.site.urls), name='admin'),
)