from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^portfolios/?', include('portfolios.urls')),

    # Examples:
    # url(r'^$', 'portfolioapp.views.home', name='home'),
    # url(r'^portfolioapp/', include('portfolioapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
