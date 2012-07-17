#-*- coding:utf-8 -*-
from django.contrib import auth

def in_editor_group(user):
#'''1st arg needs a User.'''
    if user:
        try:
            if user.groups.filter(name='editor'):
                return True
        except:
            return False
    return False
    