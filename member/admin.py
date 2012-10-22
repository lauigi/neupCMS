#-*- coding:utf-8 -*-
from django.contrib import admin
from member.models import *

admin.site.register(Member)
admin.site.register(MemberAddon)
