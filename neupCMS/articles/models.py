#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class Article(models.Model):
    aid = models.AutoField(null=False,primary_key=True)
    typeid = models.IntegerField()
    authorid = models.IntegerField()
    title = models.CharField(max_length=30)
    content = models.TextField()
    
    def __unicode__(self):
        return u'%s\n%s'%(self.title,self.content)