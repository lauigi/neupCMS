#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from neupCMS.forms import LoginForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from neupCMS.standard_test import render_test_error

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
    
def login_error(request,pwd_wrong):
    form = LoginForm(initial={'username':request.POST.get('username','')})
    #assert False
    return render_to_response('log-in.html', {'form': form,'page_title': 'log in test','pwd_wrong':pwd_wrong},context_instance=RequestContext(request))
    
def log_out(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/member/login/")