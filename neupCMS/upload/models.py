from django.db import models
from neupCMS import settings
from time import strftime,ctime,time
# Create your models here.
class ImageUpload(models.Model):
    image_path = models.ImageField(upload_to='images/%Y/%m/%d')
    original_image_name = models.CharField(max_length=30)
    aid = models.IntegerField(default=0)
    file_size = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%s'%(self.original_image_name)
        
class FileUpload(models.Model):
    file_path = models.FileField(upload_to='files/%Y/%m/%d')
    original_file_name = models.CharField(max_length=30)
    aid = models.IntegerField(default=0)
    file_size = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    senddate = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s'%(self.original_file_name)
        