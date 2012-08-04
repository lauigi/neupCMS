from django.db import models

VOTE_TYPE_CHOICES=(
    (0,u'simple one choice vote'),
    (1,u'complex vote'),
)
class VoteChoice(models.Model):
    vchid = models.AutoField(primary_key=True)
    vchtitle = models.CharField(max_length=100)
    vchdescr = models.TextField(blank=True,null=True)
    vchpic = models.CharField(max_length=100,null=True,blank=True)
    
    def __unicode__(self):
        return u'%s\n%s'%(self.vchid,self.vchtitle)
    
class VoteColumn(models.Model):
    vcid = models.AutoField(primary_key=True)
    vctitle = models.CharField(max_length=60)
    vcdescr = models.TextField(blank=True)
    is_multi = models.BooleanField()
    vcchoices = models.ManyToManyField(VoteChoice)
    
    def __unicode__(self):
        return u'%s\n%s'%(self.vcid,self.vctitle)
        
class VoteTask(models.Model):
    vid = models.AutoField(primary_key=True)
    vtitle = models.CharField(max_length=30)
    vdescr = models.TextField(blank=True)
    vtype = models.IntegerField(choices=VOTE_TYPE_CHOICES)
    vcolumn = models.ManyToManyField(VoteColumn)
    is_active = models.BooleanField()
    
    def __unicode__(self):
        return u'%s\n%s'%(self.vid,self.vtitle)
        
class VoterList(models.Model):
    sid = models.IntegerField(primary_key=True)
    sname = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u'%s\n%s'%(self.sid,self.sname)
        
#class VotedIP(models.Model):