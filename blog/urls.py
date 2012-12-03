from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blog.models import EntriesFeed

urlpatterns = patterns('blog.views',
    url(r'^archive/$', 'archive', name='archive'),
    url(r'^about/$', 'about', name='about'),
    url(r'^rss/$', EntriesFeed(), name='rss'),
    url(r'^projects/$', 'projects', name='projects'),
    url(r'^ajax/mardown_comment/$', 'markdown_comment',
            name='markdown_comment'),
    url(r'^ajax/get_comment/$', 'get_comment', name='get_comment'),
    url(r'^ajax/flag_comment/$', 'flag_comment', name='flag_comment'),
    url(r'^tag/(?P<tags>[^\.]+)/$', 'index', name='tags'),
    url(r'^(?P<slug>[^\.]+)/$', 'detail', name='detail'),
    url(r'^$', 'index', name='index'),
)

urlpatterns += staticfiles_urlpatterns()
