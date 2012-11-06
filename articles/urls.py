from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect


urlpatterns = patterns('',
    url(r'^(?P<articleid>\d+)/$', 'articles.views.show_article'),
    url(r'^(?P<articleid>\d+)/edit/$', 'articles.views.edit_article'),
    url(r'^?P<articleid>\d+)/verify/$', 'articles.views.verify_article'),
    url(r'^(?P<articleid>\d+)/resume/$', 'articles.views.resume_article'),
    url(r'^(?P<articleid>\d+)/delete/$', 'articles.views.delete_article'),
    url(r'^new/$', 'articles.views.edit_article'),

)
