from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('blog.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<entry_id>\d+)/$', 'detail', name='detail'),
    url(r'^archive/$', 'archive', name='archive'),
)
