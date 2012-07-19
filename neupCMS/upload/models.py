from django.db import models
from neupCMS import settings
from time import strftime,ctime,time
# Create your models here.
class ImageUpload(models.Model):
    image_path = models.ImageField(upload_to='images/%Y/%m/%d')
    image_name = models.CharField(max_length=30,blank=True)
    
    def __unicode__(self):
        return u'%s'%(self.image_name)
        
class FileUpload(models.Model):
    file_path = models.FileField(upload_to='files/%Y/%m/%d')
    file_name = models.CharField(max_length=30,blank=True)
    
    def __unicode__(self):
        return u'%s'%(self.file_name)
        