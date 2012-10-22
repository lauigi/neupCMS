#-*- coding:utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from member.util import render_form_page,redirect
from member.models import Member,MemberAddon
from wheel.util import is_admin
from wheel.forms import UseraddForm

@login_required
def wheel_list(request):
    if is_admin(request.user.id):
        return HttpResponse('wheel page')
    else:
        return HttpResponseRedirect('/')

@login_required
def useradd(request):
    if is_admin(request.user.id):
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
    #user = Member.objects.create_user(username, email, pw)
    #uaddon = MemberAddon(mid=user.id)
    #uaddon.save()