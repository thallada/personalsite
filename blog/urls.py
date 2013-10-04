from django.conf.urls.defaults import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blog.models import EntriesFeed
from django.views.generic import RedirectView
from django.conf import settings

urlpatterns = patterns('blog.views',
    url(r'^blog/archive/$', 'archive', name='archive'),
    url(r'^about/$', 'about', name='about'),
    url(r'^rss/$', EntriesFeed(), name='rss'),
    url(r'^projects/$', 'projects', name='projects'),
#    url(r'^resume(\.pdf)?/$', RedirectView.as_view(
#            url=settings.STATIC_URL + 'resume.pdf'), name='resume'),
#    url(r'^robots.txt/$', RedirectView.as_view(
#            url=settings.STATIC_URL + 'robots.txt'), name='robots'),
    url(r'^ajax/mardown_comment/$', 'markdown_comment',
            name='markdown_comment'),
    url(r'^ajax/get_comment/$', 'get_comment', name='get_comment'),
    url(r'^ajax/flag_comment/$', 'flag_comment', name='flag_comment'),
    url(r'^ajax/publish_draft_doc/' + settings.DRAFT_PUBLISH_KEY + '/$',
            'publish_draft_doc', name='publish_draft'),
    url(r'^blog/tag/(?P<tags>[^\.]+)/$', 'index', name='tags'),
    url(r'^blog/(?P<slug>[^\.]+)/$', 'detail', name='detail'),
    url(r'^blog/$', 'index', name='index'),
    url(r'', include('homepage.urls')),
)

urlpatterns += staticfiles_urlpatterns()
