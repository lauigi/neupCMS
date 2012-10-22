#-*- coding:utf-8 -*-
import os

from django.contrib import auth
from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import list_detail

from neupCMS.custom_proc import custom_proc
from neupCMS.settings import URL_PRE
from member.forms import LoginForm, PasswdForm
from member.models import Member, MemberAddon
from member.util import render_form_page, redirect, render_blank_page
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
            user = Member.objects.get(id=request.user.id)
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
            user = Member.objects.get(id=request.user.id)
            if user.check_password(request.POST.get('ori_password')):
                passwd = request.POST.get('password')
                user.set_password(passwd)
                user.save()
                error={'edit_success':True}
            else:
                return HttpResponse("wrong password")
    return render_form_page(request,'','passwd.html',PasswdForm,{},error)

@login_required
def profile_page(request,username):
    user=get_object_or_404(Member,username=username)
    page = request.GET.get('page','')
    profile_dict={
        'username':username,
        'email':user.email,
    }
    article_list=[{'aid':item.aid,'is_deleted':item.is_deleted,'is_verified':item.is_verified,'is_headline':item.is_headline,'title':item.title,'authorname':item.authorname,'typename':Type.objects.get(typeid=item.typeid).typename} for item in Article.objects.filter(authorname=user.username)]
    verify_auth=in_editor_group(request.user)
    resume_auth=in_admin_group(request.user)
    p = Paginator(article_list,10)
    try:
        article_list = p.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页.
        article_list = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        article_list = p.page(p.num_pages)
    return render_to_response('member-profile.html',{'profile_dict':profile_dict,
        'article_list':article_list,
        'verify_auth':verify_auth,
        'resume_auth':resume_auth,
        'page_title':username},context_instance=RequestContext(request,processors=[custom_proc]))