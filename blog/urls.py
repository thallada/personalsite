from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('blog.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<entry_id>\d+)/$', 'detail', name='detail'),
    url(r'^archive/$', 'archive', name='archive'),
)

urlpatterns += staticfiles_urlpatterns()
