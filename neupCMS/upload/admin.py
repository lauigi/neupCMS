#-*- coding:utf-8 -*-
from django.contrib import admin
from upload.models import *

admin.site.register(ImageUpload)
admin.site.register(FileUpload)
