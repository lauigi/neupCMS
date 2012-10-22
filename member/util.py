#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from neupCMS.custom_proc import custom_proc
from random import choice
import string

def render_form_page(request,next,template_name,Form,form_initial={},error={}):
    if request.method == 'POST':
        form = Form(request.POST)
    else:
        form = Form(initial=form_initial)
    return render_to_response(template_name, {'form': form,
        'error':error,
        'next':next},context_instance=RequestContext(request,processors=[custom_proc]))
        
def redirect(request,target_url=''):
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    else:
        return HttpResponseRedirect(target_url)
        
def render_blank_page(request,content=''):
    return render_to_response('blank.html', {'page_content': content},context_instance=RequestContext(request,processors=[custom_proc]))
    
def gen_random_str(length=10, chars= string.letters+string.digits):
    while True:
        yield ''.join([choice(chars) for i in range(length)])