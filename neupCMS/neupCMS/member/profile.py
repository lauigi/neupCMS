#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext,get_object_or_404
from django.contrib import auth
from django.http import HttpResponseRedirect
from neupCMS.standard_test import custom_proc
from neupCMS.member.group_auth import in_editor_group,in_admin_group
from django.contrib.auth.decorators import login_required,user_passes_test
from articles.models import Type,Article,AddonArticle

@login_required
#@user_passes_test(in_editor_group)
def profile_page(request,username):
    user=get_object_or_404(auth.models.User,username=username)
    profile_dict={
        'username':username,
        'email':user.email,
    }
    article_list=[{'aid':item.aid,'is_deleted':item.is_deleted,'is_verified':item.is_verified,'title':item.title,'authorname':item.authorname} for item in Article.objects.filter(authorname=user.username)]
    verify_auth=in_editor_group(request.user)
    resume_auth=in_admin_group(request.user)
    manage_auth=True
    #assert False
    return render_to_response('member-profile.html',{'profile_dict':profile_dict,
        'article_list':article_list,
        'verify_auth':verify_auth,
        'resume_auth':resume_auth,
        'manage_auth':manage_auth},context_instance=RequestContext(request,processors=[custom_proc]))