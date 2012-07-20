#-*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from upload.models import ImageUpload,FileUpload
from articles.models import Article,AddonArticle
from django.core.files.base import ContentFile
from time import time
from random import random

@login_required
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        max_size=4000*1024
        state="SUCCESS"
        img= request.FILES['upfile']
        title=request.POST.get('pictitle','')
        ori_name=request.POST.get('fileName','')
        if img.size > max_size:
            state=u"图片大小超出限制"
        img.name = str(time())[:-3] + str(random())[-5:] + '.'+img.name.split('.')[-1].lower()
        #assert False
        if state == "SUCCESS":
            img_uploaded = ImageUpload(image_path=img,original_image_name=ori_name,file_size=img.size)
            img_uploaded.save()
            url=img_uploaded.image_path
        json="{'url':'%s','title':'%s','original':'%s','state':'%s'}" % (url,title,ori_name,state)
    else:
        raise Http404()
    return HttpResponse(json)
    
@login_required
def upload_file(request,articleid=0):
    raise Http404()
    if request.method == 'POST':
        max_size=10*1024*1024
        allow_file_type=[".rar",".doc",".docx",".zip",".pdf",".txt",".swf",".xls",".xlsx"]
        f=request.FILES['upload_file']
        if f:
            current_type = f.name.split('.')[-1].lower()
            if f.size < max_size and current_type not in allow_file_type:
                ori_name=request.POST.get('fileName','')
                f.name = str(time())[:-3] + str(random())[-5:] + '.'+f.name.split('.')[-1].lower()
                f_uploaded = FileUpload(file_path=f,original_file_name=ori_name,file_size=f.size)
                #f_uploaded.save()
                url=f_uploaded.file_path
                json='{"state":"%s","url":"%s","fileType":"%s","original":"%s"}' % (state,url,current_type,ori_name)
            else:
                json="{'state':'文件大小超出服务器配置！','url':'null','fileType':'null'}"
    else:
        raise Http404()
    return HttpResponse(json)
    
@login_required
def upload_file_ueditor(request):
    if request.method == 'POST':
        max_size=10*1024*1024
        allow_file_type=[".rar",".doc",".docx",".zip",".pdf",".txt",".swf",".xls",".xlsx"]
        state="SUCCESS"
        f=request.FILES['upfile']
        print f
        if f:
            print 'now get the file'
            current_type = f.name.split('.')[-1].lower()
            ori_name=request.POST.get('fileName','')
            if f.size > max_size:
                state=u"文件大小超出限制"
            if current_type not in allow_file_type:
                state=u"不支持的文件类型！"
            f.name = str(time())[:-3] + str(random())[-5:] + '.'+f.name.split('.')[-1].lower()
            if state == "SUCCESS":
                f_uploaded = FileUpload(file_path=f,original_file_name=ori_name)
                f_uploaded.save()
                url=f_uploaded.file_path
            json='{"state":"%s","url":"%s","fileType":"%s","original":"%s"}' % (state,url,current_type,ori_name)
        else:
            json="{'state':'文件大小超出服务器配置！','url':'null','fileType':'null'}"
    else:
        raise Http404()
    return HttpResponse(json)