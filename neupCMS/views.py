#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext,get_object_or_404
from django.http import Http404
from articles.models import Type,Article,AddonArticle
from neupCMS.custom_proc import custom_proc
from ad.util import show_index_ad
from config.util import show_menu
from vote.util import show_simple_vote

def show_index(request):
    type_dict={}
    m=show_menu()
    types=Type.objects.all()
    for t in types:
        type_dict[t.typeid]={'t':t,'a_list':[a for a in Article.objects.filter(typeid=t.typeid).filter(is_verified=True).filter(is_deleted=False).order_by('-senddate')[:9]]}
    slideshow_article=Article.objects.filter(is_slideshow=True,is_verified=True,is_deleted=False).order_by("-senddate")[:5]
    slideshow_list=[{'aid':a.aid,'thumb_path':a.slideshow_img.thumb_path,'title':a.title} for a in slideshow_article]
    ad_list=show_index_ad()
    vlist=show_simple_vote(1)
    #assert False
    return render_to_response('index.html', {'type_dict':type_dict,
        'slideshow_list':slideshow_list,
        'ad':ad_list,
        'vlist':vlist,
        'page_title':'东北大学先锋网'},context_instance=RequestContext(request,processors=[custom_proc]))