#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class Article(models.Model):
    aid = models.AutoField(primary_key=True)
    is_verified = models.NullBooleanField()
    authorname = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    content = models.TextField()
    
    def __unicode__(self):
        return u'%s\n%s'%(self.title,self.aid)

class Type(models.Model):
    typeid = models.AutoField(null=False,primary_key=True)
    typename = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s\n%s'%(self.typeid,self.typename)
        
class AddonArticle(models.Model):
    aid = models.ForeignKey(Article,primary_key=True)
    typeid = models.IntegerField()
    senddate = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
    authorip = models.GenericIPAddressField()
    hits = models.IntegerField(default=0)
    goodpost = models.IntegerField(default=0)#顶
    baddpost = models.IntegerField(default=0)#踩
    is_headline = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s\n%s'%(self.aid,self.authorip)
        
