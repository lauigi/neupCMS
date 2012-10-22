#-*- coding:utf-8 -*-
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名',error_messages={'required': u'用户名不能为空'})
    password = forms.CharField(label=u'密码',widget=forms.PasswordInput,error_messages={'required': u'密码不能为空'})
    
class PasswdForm(forms.Form):
    ori_password = forms.CharField(label=u'原密码',widget=forms.PasswordInput,error_messages={'required': u'原密码不能为空'})
    password = forms.CharField(label=u'新密码',widget=forms.PasswordInput,error_messages={'required': u'新密码不能为空'})
    password_check = forms.CharField(label=u'再输入一次密码',widget=forms.PasswordInput,error_messages={'required': u'请重复输入'})
    
    def clean_password_check(self):
        password_check = self.cleaned_data['password_check']
        if not password_check == self.cleaned_data['password']:
            raise forms.ValidationError("两次输入不一致！")
        return password_check
        