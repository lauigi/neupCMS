#-*- coding:utf-8 -*-
from django import forms
from neupCMS.widgets import UEditor
from articles.models import Type,AddonArticle,Article
from neupCMS.util import img_from_content

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
    is_headline = forms.BooleanField(label=u'是否作为重点新闻',required=False)
    is_slideshow = forms.BooleanField(label=u'是否推送到首页图片',required=False)
    slideshow_img = forms.ChoiceField(label=u'请选择一个图片作为封面',choices=())
    
    def __init__(self, *args, **kwargs):
        super(VerifyForm, self).__init__(*args, **kwargs)
        img_list=img_from_content(kwargs['initial']['aid'])
        self.fields['slideshow_img'].choices = [('0','--------')]+[(item,i+1) for i,item in enumerate(img_list)]
    
    def clean_slideshow_img(self):
        slideshow_img = self.cleaned_data['slideshow_img']
        try:
            is_slideshow=self.is_slideshow
        except:
            is_slideshow=False
        if slideshow_img == '0' and is_slideshow:
            raise forms.ValidationError("请选择图片")
        return slideshow_img
    
class UploadForm(forms.Form):
    upfile = forms.ImageField(label=u'上传文件')