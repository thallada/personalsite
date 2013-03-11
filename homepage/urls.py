from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('homepage.views',
    url(r'^$', 'home', name='home'),
)

urlpatterns += staticfiles_urlpatterns()
