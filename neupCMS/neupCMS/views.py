#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext,get_object_or_404
from django.http import Http404
from articles.models import Type,Article,AddonArticle
from neupCMS.standard_test import custom_proc
from neupCMS.member.login import redirect

def show_index(request):
    type_list=[]
    types=Type.objects.all()
    for t in types:
        type_list.append([{'aid':item.aid,'is_deleted':item.is_deleted,'is_verified':item.is_verified,'title':item.title,'authorname':item.authorname,'senddate':item.senddate,'typename':t.typename} for item in Article.objects.filter(typeid=t.typeid)])
    #assert False
    return render_to_response('index.html', {'type_list':type_list,
        'is_index':True,
        'page_title':'东北大学先锋网'},context_instance=RequestContext(request,processors=[custom_proc]))