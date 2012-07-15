#-*- coding:utf-8 -*-

def render_test_error(request):
    '''render a template for error display'''
    return {
        'page_title': 'test',
        'ip_address': request.META['REMOTE_ADDR']
    }