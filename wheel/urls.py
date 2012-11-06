from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^useradd/$', 'wheel.views.useradd'),
    #url(r'^denied/$', 'wheel.views.wheel_list'),
    #url(r'^verify/$', 'wheel.views.wheel_list'),
    #url(r'^rabbish/$', 'wheel.views.wheel_list'),
    url(r'^list/(?P<list_method>all|deleted|verify|reject)/(?P<u>\w+)/$', 'wheel.views.list_article'),
    url(r'^list/(?P<list_method>all|deleted|verify|reject)/$', 'wheel.views.list_article'),
    url(r'^list/(?P<u>\w+)/$', 'wheel.views.list_article'),
    url(r'^list/$', 'wheel.views.list_article'),
)
