from django.conf.urls import patterns, include, url

from portfolioapp.apps.home import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name="home_index"),
    url(r'^portfolios/', include('portfolioapp.apps.portfolios.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)