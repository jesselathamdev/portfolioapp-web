from django.conf.urls import patterns, include, url

from home import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name="home_index"),
    url(r'^portfolios/', include('portfolios.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)