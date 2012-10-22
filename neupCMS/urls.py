from django.conf import settings
from django.conf.urls import patterns, include, url
from neupCMS.settings import URL_PRE
# Uncomment the next two lines to enable the admin:

if URL_PRE:
    urlpatterns = patterns('',
        url(r'^%s/'%(URL_PRE[1:]), include('neupCMS.site_urls')),
    )
else:
    urlpatterns = patterns('',
        url(r'^', include('neupCMS.site_urls')),
    )
