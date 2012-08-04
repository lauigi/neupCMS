#-*- coding:utf-8 -*-
from articles.models import Article,PostList,Type

def add_hit(articleid):
    a=Article.objects.get(aid=article)
    a.hits=a.hits+1
    a.save()
    
def format_boolean(boolean_value):
    '''看起来木有用，后期清理掉'''
    if boolean_value==u'True':
        return True
    elif boolean_value==u'False':
        return False
    else:
        return None

def get_hot_article():
    return [{'aid':item.aid,'title':item.title} for item in Article.objects.filter(is_verified=True).filter(is_deleted=False).order_by("-goodpost")[:10]]
    
def get_new_article():
    return [{'aid':item.aid,'title':item.title} for item in Article.objects.filter(is_verified=True).filter(is_deleted=False).order_by("-aid")[:10]]
    
def get_unverified_article():
    return [{'aid':item.aid,
        'is_deleted':item.is_deleted,
        'is_verified':item.is_verified,
        'is_headline':item.is_headline,
        'title':item.title,
        'authorname':item.authorname,
        'typename':Type.objects.get(typeid=item.typeid).typename} for item in Article.objects.filter(is_verified=False).filter(is_deleted=False)]
        
def get_recycled_article():
    return [{'aid':item.aid,
        'is_deleted':item.is_deleted,
        'is_verified':item.is_verified,
        'is_headline':item.is_headline,
        'title':item.title,
        'authorname':item.authorname,
        'typename':Type.objects.get(typeid=item.typeid).typename} for item in Article.objects.filter(is_deleted=True)]