#-*- coding:utf-8 -*-
from ad.models import Index_AD

def show_index_ad():
    adlist=[{'title':item.title,'link':item.link,'img':item.img} for item in Index_AD.objects.filter(is_active=True).order_by('-id')[:5]]
    return adlist