#-*- coding:utf-8 -*-
from django import forms
from widgets import UEditor
from articles.models import Type,Article,AddonArticle

class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名',error_messages={'required': u'用户名不能为空'})
    password = forms.CharField(label=u'密码',widget=forms.PasswordInput,error_messages={'required': u'密码不能为空'})
    
class EditForm(forms.Form):
    
    title = forms.CharField(label=u'文章标题',max_length=30,error_messages={'required': u'文章标题不能为空','max_length':u'标题过长，请修改'})
    typeid = forms.ChoiceField(label=u'分类',choices=())
    #u_text = forms.CharField(label=u'文章内容',widget=forms.Textarea,error_messages={'required': u'文章内容不能为空'})
    u_text = forms.CharField(label=u'正文',widget=UEditor(),error_messages={'required': u'文章内容不能为空'})
    
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['typeid'].choices = [('0','--------')]+[(item.typeid,item.typename) for item in Type.objects.all()]
        
    def clean_typeid(self):
        typeid = self.cleaned_data['typeid']
        if typeid == '0':
            raise forms.ValidationError("请选择分类")
        return typeid
        
class VerifyForm(forms.Form):
    is_verified = forms.TypedChoiceField(label=u'审核',choices=[(None,u'未审核'),(True,u'审核通过'),(False,u'未通过审核')])
    
class UploadForm(forms.Form):
    upload_file = forms.FileField(label=u'上传文件')