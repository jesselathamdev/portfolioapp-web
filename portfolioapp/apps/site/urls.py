from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'portfolioapp.apps.site.views.home_index', name='home_index'),
)