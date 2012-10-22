#-*- coding:utf-8 -*-
from django.contrib import auth

def in_editor_group(user):
#'''1st arg needs a User.'''
    if user:
        try:
            if user.is_staff or user.is_admin:
                return True
        except:
            return False
    return False
    
def in_admin_group(user):
    if user:
        try:
            if user.is_admin:
                return True
        except:
            return False
    return False
    