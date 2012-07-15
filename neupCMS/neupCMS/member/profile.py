#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from neupCMS.standard_test import render_test_error
from django.contrib.auth.decorators import login_required

def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/member/profile/%s/"%(user.username))
            else:
                return login_error(request,pwd_wrong=True)
    else:
        form = LoginForm()
    return render_to_response('log-in.html', {'form': form,'page_title': 'log in test'},context_instance=RequestContext(request))

@login_required
def profile_page(request,username):
    profile_list={
        'username':username,
    }
    return render_to_response('member-profile.html',{'profile_list':profile_list},context_instance=RequestContext(request))