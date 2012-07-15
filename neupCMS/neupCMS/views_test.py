#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from neupCMS.forms import LoginForm
from django.contrib import auth


def hello(request):
    return HttpResponse("Hello world")
    
def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))