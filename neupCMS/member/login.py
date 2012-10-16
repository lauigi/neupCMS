#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext
from neupCMS.forms import LoginForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from neupCMS.custom_proc import custom_proc

def log_in(request):
    if not request.user.is_authenticated():
        next=''
        if request.GET.get('next'):
            next='?next='+request.GET.get('next')
        if request.method == 'POST':
            form = LoginForm(request.POST)
            e=form.errors
            #assert False
            if form.is_valid():
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    return redirect(request,"/member/profile/%s/"%(user.username))
                else:
                    return render_login(request,next,pwd_wrong=True)
        return render_login(request,next)
    else:
        return redirect(request,"/member/profile/%s/"%(request.user.username))
    
def render_login(request,next,pwd_wrong=False):
    if request.method == 'POST':
        form = LoginForm(request.POST)
    else:
        form = LoginForm()
    return render_to_response('log-in.html', {'form': form,
        'page_title': 'log in test',
        'pwd_wrong':pwd_wrong,
        'next':next},context_instance=RequestContext(request,processors=[custom_proc]))

def log_out(request):
    auth.logout(request)
    return redirect(request,'/member/login/')
    
def redirect(request,target_url=''):
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    else:
        return HttpResponseRedirect(target_url)