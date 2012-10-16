#-*- coding:utf-8 -*-
from django.db import models
from upload.models import FileUpload,ImageUpload

# Create your models here.
class Article(models.Model):
    aid = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.NullBooleanField()
    authorname = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    hits = models.IntegerField(default=0)
    goodpost = models.IntegerField(default=0)#顶
    baddpost = models.IntegerField(default=0)#踩
    is_headline = models.NullBooleanField(default=False)
    is_slideshow = models.NullBooleanField(default=False)
    typeid = models.IntegerField()
    senddate = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
    slideshow_img = models.ForeignKey(ImageUpload,null=True)
    
    def __unicode__(self):
        return u'%s\n%s'%(self.title,self.aid)

class Type(models.Model):
    typeid = models.AutoField(null=False,primary_key=True)
    typename = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s\n%s'%(self.typeid,self.typename)
        
class AddonArticle(models.Model):
    aid = models.AutoField(primary_key=True)
    content = models.TextField()
    authorip = models.GenericIPAddressField()
    attachments = models.ManyToManyField(FileUpload)
    
    def __unicode__(self):
        return u'%s\n%s'%(self.aid,self.authorip)
        
class PostList(models.Model):
    aid = models.IntegerField()
    poster_ip = models.GenericIPAddressField()
    
    def __unicode__(self):
        return u'%s\n%s'%(self.aid,self.poster_ip)