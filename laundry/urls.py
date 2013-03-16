from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('laundry.views',
    url(r'^ajax/current/(?P<hall>\d+)/$', 'ajax_get_current', name='get_current_chart'),
    url(r'^$', 'main_page', name='laundry_main'),
)
