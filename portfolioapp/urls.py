from django.conf.urls import patterns, include, url
from django.contrib import admin

from portfolioapp.apps.home import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sign-in/$', 'django.contrib.auth.views.login', {'template_name': 'signin.html'}),

    url(r'^$', views.index, name="home_index"),
    url(r'^portfolios/', include('portfolioapp.apps.portfolios.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)