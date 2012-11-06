#-*- coding:utf-8 -*-
from member.models import Member
from django.shortcuts import get_object_or_404

def check_article(a, list_method, verify_auth, resume_auth):
    if list_method=='deleted':
        return a.is_deleted and resume_auth
    elif list_method=='verify':
        return a.is_verified==None
    elif list_method=='reject':
        return a.is_verified==False
    else:
        return not a.is_deleted or resume_auth