#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from neupCMS.standard_test import custom_proc
from neupCMS.member.group_auth import in_editor_group
from django.contrib.auth.decorators import login_required,user_passes_test


@login_required
#@user_passes_test(in_editor_group,login_url='/hello/')
def profile_page(request,username):
    profile_list={
        'username':username,
        #'is_editor':'经过身份验证，你是编辑',
    }
    return render_to_response('member-profile.html',{'profile_list':profile_list},context_instance=RequestContext(request,processors=[custom_proc]))