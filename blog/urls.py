from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blog.models import EntriesFeed

urlpatterns = patterns('blog.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<entry_id>\d+)/$', 'detail', name='detail'),
    url(r'^archive/$', 'archive', name='archive'),
    url(r'^about/$', 'about', name='about'),
    url(r'^rss/$', EntriesFeed(), name='rss'),
    url(r'^ajax/mardown_comment/$', 'markdown_comment',
            name='markdown_comment'),
)

urlpatterns += staticfiles_urlpatterns()
