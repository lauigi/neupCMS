from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/$', 'member.views.login'),
    url(r'^logout/$', 'member.views.logout'),
    url(r'^passwd/$', 'member.views.passwd'),
    url(r'^profile/(?P<username>\w+)/$', 'member.views.profile_page'),
)
