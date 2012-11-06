#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from neupCMS.util import render_form_page,redirect, pag
from neupCMS.custom_proc import custom_proc
from member.models import Member,MemberAddon
from member.group_auth import in_editor_group, in_admin_group
from wheel.util import check_article
from wheel.forms import UseraddForm
from articles.models import Article,Type

#@login_required


@login_required
def list_article(request, u='', list_method='all'):
    verify_auth=in_editor_group(request.user)
    if not verify_auth:
        return Http404()

    resume_auth=in_admin_group(request.user)
    list_all = False

    if not u or u == request.user.username or u==request.user.id:
        user = request.user
        is_self = True
        if not u:
            list_all = True
    else:
        try:
            user = Member.objects.get(id=u)
        except:
            user = get_object_or_404(Member,username=u)
            
    page = request.GET.get('page','')
    
    if list_all:
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(authorname=user.username)
    article_list = [{'aid':a.aid, 'is_deleted':a.is_deleted,
        'is_verified':a.is_verified, 'is_headline':a.is_headline,
        'title':a.title, 'authorname':a.authorname,
        'typename':Type.objects.get(typeid=a.typeid).typename} 
        for a in articles if check_article(a,list_method,verify_auth,resume_auth)]
    article_list = pag(article_list,page,20)
    list_method_dict = {list_method:1}
    return render_to_response('wheel/list-article.html',{'article_list':article_list,
        'resume_auth':resume_auth,
        'verify_auth':verify_auth,
        'user':user,
        'list_all':list_all,
        'method':list_method_dict,
        'page_title':u'article manage'},context_instance=RequestContext(request,processors=[custom_proc]))

@login_required
def useradd(request):
    if in_admin_group(request.user):
        error={}
        if request.method == 'POST':
            form = UseraddForm(request.POST)
            if form.is_valid():
                post_data=form.cleaned_data
                username,pw,email,nickname = post_data['username'],post_data['password'],post_data['email'],post_data['nickname']
                try:
                    user = Member.objects.create_user(username, email, pw)
                    user.nickname=nickname
                    uaddon = MemberAddon(mid=user.id)
                    user.save()
                    uaddon.save()
                    return redirect(request,'/wheel/')
                except:
                    error['name_wrong']=True#实际上也可能会是邮箱出错
        return render_form_page(request,'','wheel/useradd.html',UseraddForm,{},error)
    else:
        return HttpResponseRedirect('/')