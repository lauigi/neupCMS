#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import (check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from django.utils import timezone
from django.core.mail import send_mail

        
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10,unique=True)#登录时使用的用户名
    nickname = models.CharField(max_length=30,blank=True)#主要的显示名称
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()

    def __unicode__(self):
        return self.nickname

    def natural_key(self):
        return (self.username,)

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()
        return check_password(raw_password, self.password, setter)

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
#=============================================================#
    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self, perm, obj)

class MemberAddon(models.Model):
    mid = models.AutoField(primary_key=True)
    age = models.IntegerField(blank=True,default=0)
    
