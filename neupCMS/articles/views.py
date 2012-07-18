#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext,get_object_or_404
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required,user_passes_test
from neupCMS.forms import EditForm,VerifyForm
from articles.models import Type,Article,AddonArticle
from neupCMS.standard_test import custom_proc
from neupCMS.member.group_auth import in_editor_group,in_admin_group
from neupCMS.member.login import redirect
#from django.template import loader


def show_article(request,articleid,edited=False,no_perm=False,verify=False,verify_form=None):
    a = get_object_or_404(Article, aid=articleid)
    if not in_editor_group(request.user) and verify:
        verify=False
        no_perm=True
    if verify:
        t=a.is_verified
        #assert False
        verify_form=VerifyForm(initial={'is_verified':a.is_verified})
    if a.is_verified or in_editor_group(request.user) or request.user.username==a.authorname:
        if not a.is_deleted or in_admin_group(request.user):
            a_addon = AddonArticle.objects.get(aid_id=articleid)
            type = Type.objects.get(typeid=a.typeid)
            return render_to_response('show-article.html', {'article':a,
                'addon_article':a_addon,
                'type':type,
                'no_perm':no_perm,
                'edited':edited,
                'verify':verify,
                'verify_form':verify_form,
                'page_title':a.title},context_instance=RequestContext(request,processors=[custom_proc]))
        else:
            raise Http404()
    else:
        raise Http404()
        
def list_by_type(request,typeid):
    t = get_object_or_404(Type, typeid=typeid)
    article_list=[{'aid':item.aid,'is_deleted':item.is_deleted,'is_verified':item.is_verified,'title':item.title,'authorname':item.authorname,'senddate':item.senddate} for item in Article.objects.filter(typeid=t.typeid)]
    #assert False
    return render_to_response('article-list-by-type.html', {'article_list':article_list,
        'type':{'typeid':t.typeid,'typename':t.typename},
        'page_title':t.typename},context_instance=RequestContext(request,processors=[custom_proc]))
    
@login_required
def edit_article(request,articleid=0):
    result_aid=False
    if request.method == 'POST':
        if request.POST.get('is_verified') and in_editor_group(request.user):
            is_verified=format_is_verified(request.POST.get('is_verified'))
            a = get_object_or_404(Article, aid=articleid)
            a.is_verified=is_verified
            a.save()
            t=a.is_verified
            #assert False
            return show_article(request,articleid,edited=True)
        else:
            form = EditForm(request.POST)
            if form.is_valid():
                return update_article(request,articleid)
    else:
        if articleid==0:
            form = EditForm()
        else:
            a = get_object_or_404(Article, aid=articleid)
            if request.user.username==a.authorname or in_editor_group(request.user):
                a_addon = AddonArticle.objects.get(aid_id=articleid)
                form = EditForm(initial={'title':a.title,
                    'typeid':a.typeid,
                    'u_text':a_addon.content})
            else:
                return show_article(request,articleid,no_perm=True)    
    return render_to_response('edit-article.html', {'form': form,
        'page_title': 'add article test',
        'result_aid':result_aid,
        'aid':articleid},context_instance=RequestContext(request,processors=[custom_proc]))
        
@login_required
def delete_article(request,articleid):
    a = get_object_or_404(Article, aid=articleid)
    if request.user.username==a.authorname or in_editor_group(request.user):
        a.is_deleted=True
        a.save()
        return redirect(request,'/member/profile/%s/'%(a.authorname))#目前还没法在重定向的页面中提示删除成功，待完善
    else:
        return show_article(request,articleid,no_perm=True)
        
@login_required
def resume_article(request,articleid):
    '''可以与delete_article重构为同一个视图'''
    a = get_object_or_404(Article, aid=articleid)
    if in_admin_group(request.user):
        a.is_deleted=False
        a.save()
        return redirect(request,'/member/profile/%s/'%(a.authorname))
    else:
        raise Http404()

def update_article(request,articleid=0):
    typeid = request.POST.get('typeid', '')
    title = request.POST.get('title', '')
    u_text = request.POST.get('u_text', '')
    if articleid==0:
        a = Article(title=title,
            typeid=typeid,
            authorname=request.user.username)
        a.save()
        a_addon = AddonArticle(aid_id=a.aid,
            content=u_text,
            authorip=request.META['REMOTE_ADDR'])
        a_addon.save()
    else:
        a = get_object_or_404(Article, aid=articleid)
        if request.user.username==a.authorname or in_editor_group(request.user):
            a.title = title
            a.typeid = typeid
            a_addon = AddonArticle.objects.get(aid_id=articleid)
            a_addon.content = u_text
            a.save()
        else:
            return show_article(request,articleid,no_perm=True)
    return show_article(request,a.aid,edited=True)
    
def format_is_verified(is_verified):
    #assert False
    if is_verified==u'True':
        return True
    elif is_verified==u'False':
        return False
    else:
        return None
        