from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('laundry.views',
    url(r'^$', 'main_page', name='laundry_main'),
)
