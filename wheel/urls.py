from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^useradd/$', 'wheel.views.useradd'),
    url(r'^$', 'wheel.views.wheel_list'),
)
