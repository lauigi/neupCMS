from django.conf import settings
from django.conf.urls import patterns, include, url
from neupCMS.views import *
from neupCMS.views_test import *
from django.contrib.auth.views import login, logout
from neupCMS.member import login, profile
from django.http import HttpResponseRedirect

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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^member/profile/(?P<username>\w+)/$', profile.profile_page),
    url(r'^member/login/$', login.log_in),
    url(r'^accounts/login/$', login.log_in),
    url(r'^member/logout/$', login.log_out),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^hello/', hello),
        url(r'^test/display-meta/', display_meta),
        url(r'^account/loggedin/$', hello),
    )
