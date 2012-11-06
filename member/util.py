#-*- coding:utf-8 -*-

from random import choice
import string
    
def gen_random_str(length=10, chars = string.letters+string.digits):
    while True:
        yield ''.join([choice(chars) for i in range(length)])