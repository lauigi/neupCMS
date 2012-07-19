#-*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from upload.models import ImageUpload
from django.core.files.base import ContentFile
from time import time
from random import random

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        max_size=4000*1024
        state="SUCCESS"
        img= request.FILES['upfile']
        if img.size > max_size:
            state=u"图片大小超出限制"
        img.name = str(random())[-5:]+str(time())[:-3] + '.'+img.name.split('.')[-1]
        #assert False
        if state == "SUCCESS":
            img_uploaded = ImageUpload(image_path=img)
            img_uploaded.save()
            url=img_uploaded.image_path
        json="{'url':'%s','title':'%s','original':'%s','state':'%s'}" % (url,img.name,request.FILES['upfile'].name,state)
    else:
        raise Http404()
    return HttpResponse(json)