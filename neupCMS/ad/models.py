from django.db import models

# Create your models here.
class Index_AD(models.Model):
    is_active = models.BooleanField()
    title = models.CharField(max_length=30)
    link = models.CharField(max_length=100,blank=True)
    img = models.ImageField(upload_to='ad/%Y/%m/')
    
    def __unicode__(self):
        return u'%s\n%s'%(self.id,self.title)