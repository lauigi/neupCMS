#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from neupCMS.forms import EditForm
from articles.models import Type,Article,AddonArticle
from neupCMS.standard_test import custom_proc
#from django.template import loader


def show_article(request,aid,edited=False,no_perm=False):
    a = get_object_or_404(Article, aid__iexact=aid)
    a_addon = AddonArticle.objects.get(aid_id=aid)
    type = Type.objects.get(typeid=a_addon.typeid)
    return render_to_response('show-article.html', {'article':a,
        'addon_article':a_addon,
        'type':type,
        'no_perm':no_perm,
        'edited':edited,
        'page_title':a.title},context_instance=RequestContext(request,processors=[custom_proc]))
    
@login_required
def edit_article(request,aid=0):
    result_aid=False
    if request.method == 'POST':
        return update_article(request,aid)
    if aid==0:
        form = EditForm()
    else:
        a = get_object_or_404(Article, aid__iexact=aid)
        a_addon = AddonArticle.objects.get(aid_id=aid)
        form = EditForm(initial={'title':a.title,
            'typeid':a_addon.typeid,
            'u_text':a.content})
    
    return render_to_response('edit-article.html', {'form': form,
        'page_title': 'add article test',
        'result_aid':result_aid,
        'aid':aid},context_instance=RequestContext(request,processors=[custom_proc]))

def update_article(request,articleid=0):
    typeid = request.POST.get('typeid', '')
    title = request.POST.get('title', '')
    u_text = request.POST.get('u_text', '')
    if articleid==0:
        a = Article(title=title,
            content=u_text,
            authorname=request.user.username)
        a.save()
        a_addon = AddonArticle(aid_id=a.aid,
            typeid=typeid,
            authorip=request.META['REMOTE_ADDR'])
        a_addon.save()
    else:
        a = get_object_or_404(Article, aid=articleid)
        if request.user.username==a.authorname or request.user.groups.filter(name='editor') or request.user.groups.filter(name='admin'):
            a.title = title
            a.content=u_text
            a.save()
            t=a.title
            AddonArticle.objects.filter(aid_id=articleid).update(typeid=typeid)
        else:
            return show_article(request,articleid,no_perm=True)
    return show_article(request,articleid,edited=True)