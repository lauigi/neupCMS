#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
import MySQLdb
from neupCMS_config import db_config

def hello(request):
    return HttpResponse("Hello world")

def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def sql_test(request):
    db = MySQLdb.connect(host=db_config['host'],db=db_config['db'],charset=db_config['charset'],user=db_config['user'],passwd=db_config['passwd'])
    cursor = db.cursor()
    cursor.execute('SELECT name FROM test ORDER BY id')
    names = [row[0] for row in cursor.fetchall()]
    db.close()
    return render_to_response('sign-up-test.html',{'names':names,'page_title':'sql_test'})