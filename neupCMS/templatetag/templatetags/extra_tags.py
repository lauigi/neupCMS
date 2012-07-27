from django import template

register = template.Library()

@register.filter(name='short')
def short(value,lens):
    if len(value)>int(lens):
        value=value[:int(lens)]+'...'
    return value