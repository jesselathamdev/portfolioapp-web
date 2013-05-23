from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.site.views.site_index', name='site_index'),
)