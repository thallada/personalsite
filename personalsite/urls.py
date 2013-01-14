from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'', include('blog.urls')),
)
