#-*- coding:utf-8 -*-
from django.contrib import admin
from vote.models import *

admin.site.register(VoteTask)
admin.site.register(VoteColumn)
admin.site.register(VoteChoice)