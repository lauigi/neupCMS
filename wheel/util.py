#-*- coding:utf-8 -*-
from member.models import Member
from django.shortcuts import get_object_or_404

def is_admin(target_id):
    m = get_object_or_404(Member,id=target_id)
    return m.is_superuser