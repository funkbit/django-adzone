from django.conf.urls.defaults import *

urlpatterns = patterns('adzone.views',
    url(r'^view/(?P<id>[\d]+)/$', 'ad_view', name='adzone_ad_view'),
)
