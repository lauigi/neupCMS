#-*- coding:utf-8 -*-
from vote.models import VoteChoice,VoteColumn,VoteTask
#from django.shortcuts import render_to_response,RequestContext,get_object_or_404

def show_simple_vote(vid):
    try:
        v=VoteTask.objects.get(vid=vid)
    except:
        return False
    if v.vtype==1 or not v.is_active:
        return False
    vlist={'v':{'vtitle':v.vtitle,'vdescr':v.vdescr}}
    vlist['vcolumn']=[]
    for vcolumn in v.vcolumn.all():
        vlist['vcolumn'].append({'vcid':vcolumn.vcid,'vctitle':vcolumn.vctitle,'is_multi':vcolumn.is_multi,'vcchoices':[{'vchid':item.vchid,'vchtitle':item.vchtitle} for item in vcolumn.vcchoices.all()]})
    return vlist