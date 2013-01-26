from django.conf.urls import patterns, include, url
from django.contrib import admin

from portfolioapp.apps.home import views

admin.autodiscover()

urlpatterns = patterns('',
    # profiles (sign in, profile, etc)
    url(r'^sign-in/$', 'django.contrib.auth.views.login', {'template_name': 'profiles/signin.html'}, name='signin'),
    url(r'^sign-out/$', 'django.contrib.auth.views.logout', {'template_name': 'profiles/signout.html'}, name='signout'),
    url(r'^profile/$', 'portfolioapp.apps.profiles.views.profile_edit', name='profile_edit'),

    # home page
    url(r'^$', views.index, name="home_index"),

    # transactions through portfolios
    url(r'^transactions/', 'portfolioapp.apps.portfolios.views.transaction_list_index', name='transaction_list_index'),

    # portfolios
    url(r'^portfolios/', include('portfolioapp.apps.portfolios.urls')),

    # django admin
    url(r'^admin/', include(admin.site.urls), name='admin'),
)