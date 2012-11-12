from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('blog.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<entry_id>\d+)/$', 'detail', name='detail'),
    url(r'^archive/$', 'archive', name='archive'),
    url(r'^about/$', 'about', name='about'),
    url(r'^ajax/mardown_comment/$', 'markdown_comment', name='markdown_comment'),
    url(r'^ajax/get_comment/$', 'get_comment', name='get_comment'),
    url(r'^ajax/flag_comment/$', 'flag_comment', name='flag_comment'),
)

urlpatterns += staticfiles_urlpatterns()
