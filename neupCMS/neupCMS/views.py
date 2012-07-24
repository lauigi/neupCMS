#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext,get_object_or_404
from django.http import Http404
from articles.models import Type,Article,AddonArticle
from neupCMS.standard_test import custom_proc
from neupCMS.member.login import redirect
from ad.util import show_index_ad

def show_index(request):
    type_list=[]
    types=Type.objects.all()
    for t in types:
        type_list.append([{'typeid':t.typeid,'typename':t.typename,'article_list':{'aid':item.aid,'is_deleted':item.is_deleted,'is_verified':item.is_verified,'title':item.title,'authorname':item.authorname,'senddate':item.senddate,'is_headline':item.is_headline}} for item in Article.objects.filter(typeid=t.typeid)])
    slideshow_article=Article.objects.filter(is_slideshow=True,is_verified=True,is_deleted=False).order_by("-senddate")[:5]
    slideshow_list=[{'aid':a.aid,'thumb_path':a.slideshow_img.thumb_path,'title':a.title} for a in slideshow_article]
    ad_list=show_index_ad()
    return render_to_response('index.html', {'type_list':type_list,
        'is_index':True,
        'slideshow_list':slideshow_list,
        'ad':ad_list,
        'page_title':'东北大学先锋网'},context_instance=RequestContext(request,processors=[custom_proc]))