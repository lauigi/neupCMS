#-*- coding:utf-8 -*-
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名')
    password = forms.CharField(label=u'密码',widget=forms.PasswordInput)