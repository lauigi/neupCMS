from django.db import models

# Create your models here.
class Menu(models.Model):
    menuid = models.AutoField(primary_key=True)
    menu_name = models.CharField(max_length=30)
    parent_id = models.IntegerField(default=0)
    menu_link = models.CharField(max_length=60,null=True,blank=True)
    
    def __unicode__(self):
        return u'%s->%s %s'%(self.parant_id,self.menuid,self.menu_name)