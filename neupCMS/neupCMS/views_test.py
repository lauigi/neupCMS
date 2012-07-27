#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from neupCMS.forms import LoginForm,UploadForm
from django.contrib import auth
from upload.views import upload_image
from neupCMS.custom_proc import custom_proc

def hello(request):
    return HttpResponse("Hello world")
    
def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
    
def img_test(request):
    if request.method=='POST':
        form=UploadForm(request.POST)
        if form.is_valid:
            return upload_image(request)
    form=UploadForm()
    return render_to_response('test.html', {'form':form,
        'page_title':'东北大学先锋网'},context_instance=RequestContext(request,processors=[custom_proc]))
        