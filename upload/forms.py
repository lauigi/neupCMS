#-*- coding:utf-8 -*-
from django import forms
from neupCMS.util import img_from_content

class UploadForm(forms.Form):
    upfile = forms.ImageField(label=u'上传文件')