#-*- coding:utf-8 -*-
import os

from django.contrib import auth
from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.views.generic import list_detail

from neupCMS.custom_proc import custom_proc
from neupCMS.settings import URL_PRE
from member.forms import LoginForm, PasswdForm,EditProfileForm
from member.models import Member, MemberAddon
from neupCMS.util import render_form_page, redirect, render_blank_page, pag
from member.group_auth import in_editor_group, in_admin_group

from articles.models import Type,Article,AddonArticle

def whereami(request):
    if 'HOSTNAME' in os.environ:
        return HttpResponse("This is * server environ")
    else:
        return HttpResponse("This is local environ")

def login(request):
    if not request.user.is_authenticated():
        next=''
        if request.GET.get('next'):
            next='?next='+request.GET.get('next')
        if request.method == 'POST':
            form = LoginForm(request.POST)
            e=form.errors
            if form.is_valid():
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    return redirect(request,URL_PRE+"/")
                else:
                    return render_form_page(request,next,'login.html',LoginForm,error={'pwd_wrong':True})
        return render_form_page(request,next,'login.html',LoginForm)
    else:
        return redirect(request,URL_PRE+"/")

def logout(request):
    auth.logout(request)
    return redirect(request,URL_PRE+"/")

@login_required
def edit_profile(request):
    error={}
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            email,nickname = request.POST.get('email'),request.POST.get('nickname')
            user = request.user
            user.email,user.nickname = email,nickname
            user.save()
            error={'edit_success':True}

    return render_form_page(request,'','edit-profile.html',EditProfileForm,{'email':request.user.email,'nickname':request.user.nickname},error)

@login_required
def passwd(request):
    error={}
    if request.method == 'POST':
        form = PasswdForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(request.POST.get('ori_password')):
                passwd = request.POST.get('password')
                user.set_password(passwd)
                user.save()
                error={'edit_success':True}
            else:
                return HttpResponse("wrong password")
    return render_form_page(request,'','passwd.html',PasswdForm,{},error)

@login_required
def profile_page(request, username='', ):
    if not username or username == request.user.username or username==request.user.id:
        user = request.user
        is_self = True
    else:
        try:
            user = Member.objects.get(id=username)
        except:
            user = get_object_or_404(Member,username=username)
    page = request.GET.get('page','')
    profile_dict={
        'id':user.id,
        'username':user.username,
        'nickname':user.nickname,
        'email':user.email,
    }
    verify_auth=in_editor_group(request.user)
    resume_auth=in_admin_group(request.user)
    article_list = [{'aid':a.aid, 'is_deleted':a.is_deleted,
        'is_verified':a.is_verified, 'is_headline':a.is_headline,
        'title':a.title, 'authorname':a.authorname,
        'typename':Type.objects.get(typeid=a.typeid).typename} 
        for a in Article.objects.filter(authorname=user.username) 
        if (not a.is_deleted or resume_auth) and 
        (a.is_verified or verify_auth or a.authorname==request.user.username)]
    article_list = pag(article_list,page,20)
    return render_to_response('member-profile.html',{'profile_dict':profile_dict,
        'article_list':article_list,
        'verify_auth':verify_auth,
        'resume_auth':resume_auth,
        'page_title':user.username},context_instance=RequestContext(request,processors=[custom_proc]))