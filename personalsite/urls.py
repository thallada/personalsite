from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    #url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^laundry/', include('laundry.urls')),
#    url(r'^favicon\.png$', RedirectView.as_view(
#            url=settings.STATIC_URL + 'img/favicon.png'), name='favicon'),
    url(r'', include('blog.urls')),
)

urlpatterns += staticfiles_urlpatterns()
