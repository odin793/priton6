from django.conf.urls import patterns, include, url
from priton.views import *
from django.conf import settings
from django.views.decorators.cache import cache_page
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'priton6.views.home', name='home'),
    # url(r'^priton6/', include('priton6.foo.urls')),
    (r'^$', main_redirect),
    url(r'^(patients)/$', cache_page(60*15)(persons_list), name='patients_list'),
    url(r'^(doctors)/$', persons_list),
    url(r'^comics/$', comics_list),
    url('^comics/(\d+)/$', comics, name='single_comics'),
    url(r'^random/$', bla),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
