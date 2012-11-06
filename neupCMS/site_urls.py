from django.conf import settings
from django.conf.urls import patterns, include, url
from neupCMS.views import show_index
from neupCMS.views_test import *
from django.http import HttpResponseRedirect
from articles.views import *
from upload.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'neupCMS.views.home', name='home'),
    # url(r'^neupCMS/', include('neupCMS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', show_index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^member/', include('member.urls')),
    url(r'^wheel/', include('wheel.urls')),
    url(r'^article/', include('articles.urls')),
    url(r'^type/(?P<typeid>\d+)/$', list_by_type),
    url(r'^article/(?P<articleid>\d+)/upload/$', upload_file),
    url(r'^article/new/upload/$', upload_file),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^upload/images/$', upload_image),
    url(r'^upload/files/$', upload_file),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^hello/', hello),
        url(r'^test/display-meta/', display_meta),
        url(r'^test/i/$', img_test),
        url(r'^account/loggedin/$', hello),
    )
