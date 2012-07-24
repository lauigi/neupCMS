#-*- coding:utf-8 -*-
from config.util import show_menu

def custom_proc(request):
    '''render a template for error display'''
    return {
        'page_title': 'test',
        'ip_address': request.META['REMOTE_ADDR'],
        'path': request.path,
        'bool_field':[True,False,None],
        'menu_list':show_menu()
    }