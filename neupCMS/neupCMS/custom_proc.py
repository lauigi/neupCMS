#-*- coding:utf-8 -*-
from config.util import show_menu
from articles.util import get_hot_article

def custom_proc(request):
    '''render a template for error display'''
    return {
        'page_title': 'test',
        'ip_address': request.META['REMOTE_ADDR'],
        'path': request.path,
        'hot': get_hot_article(),
        'menu_list':show_menu()
    }