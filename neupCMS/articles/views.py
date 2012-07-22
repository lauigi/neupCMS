#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext,get_object_or_404
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required,user_passes_test
from neupCMS.forms import EditForm,VerifyForm,UploadForm
from articles.models import Type,Article,AddonArticle
from upload.models import ImageUpload
from neupCMS.standard_test import custom_proc
from neupCMS.member.group_auth import in_editor_group,in_admin_group
from neupCMS.member.login import redirect
from config.views import show_menu
from neupCMS.util import sort_img

def show_article(request,articleid,status={},verify_form=None):
    a = get_object_or_404(Article, aid=articleid)
    if a.is_verified or in_editor_group(request.user) or request.user.username==a.authorname:
        if not a.is_deleted or in_admin_group(request.user):
            a_addon = AddonArticle.objects.get(aid=articleid)
            type = Type.objects.get(typeid=a.typeid)
            menu_list=show_menu()
            return render_to_response('show-article.html', {'article':a,
                'addon_article':a_addon,
                'type':type,
                'status':status,
                'verify_form':verify_form,
                'page_title':a.title},context_instance=RequestContext(request,processors=[custom_proc]))

@login_required                
def verify_article(request,articleid,status={}):
    if not in_editor_group(request.user):
        status={'no_perm':True}
        return show_article(request,articleid,status)
    else:
        a = get_object_or_404(Article, aid=articleid)
        if request.method=='POST':
            form = VerifyForm(request.POST,initial={'aid':a.aid})
            if form.is_valid():
                is_verified=format_boolean(request.POST.get('is_verified'))
                is_headline=request.POST.get('is_headline')
                is_slideshow=request.POST.get('is_slideshow')
                slideshow_img=request.POST.get('slideshow_img')
                a.is_verified=is_verified
                a.is_headline=is_headline
                a.is_slideshow=is_slideshow
                if is_slideshow and slideshow_img is not '0':
                    a.slideshow_img=ImageUpload.objects.get(thumb_path=slideshow_img)
                a.save()
                status={'be_verified':True}
                return show_article(request,articleid,status)
            else:
                status['verify_failed']=True
                status['to_verify']=True
                verify_form=VerifyForm(request.POST,initial={'aid':a.aid})
                return show_article(request,articleid,status,verify_form)
        else:
            thumb_path=''
            if a.is_slideshow:
                thumb_path=a.slideshow_img.thumb_path
            verify_form=VerifyForm(initial={'is_verified':a.is_verified,
                'is_headline':a.is_headline,
                'is_slideshow':a.is_slideshow,
                'aid':a.aid,
                'slideshow_img':thumb_path})
            status={'to_verify':True}
        return show_article(request,articleid,status,verify_form)

        
#def show_attachment(articleid):
#    a_addon = get_object_or_404(AddonArticle, aid=articleid)
#    attachments_list=[]
#    attachments_list=[{'original_file_name':a_addon.original_file_name,'file_path':a_addon.file_path,'file_size':a_addon.file_size} for item in a_addon.attachments.filter(is_deleted=False)]
#    return attachments_list
        
def list_by_type(request,typeid):
    t = get_object_or_404(Type, typeid=typeid)
    menu_list=show_menu()
    article_list=[{'aid':item.aid,'is_deleted':item.is_deleted,'is_verified':item.is_verified,'title':item.title,'authorname':item.authorname,'senddate':item.senddate,'is_headline':item.is_headline} for item in Article.objects.filter(typeid=t.typeid)]
    return render_to_response('article-list-by-type.html', {'article_list':article_list,
        'type':{'typeid':t.typeid,'typename':t.typename},
        'menu_list':menu_list,
        'page_title':t.typename},context_instance=RequestContext(request,processors=[custom_proc]))
    
@login_required
def edit_article(request,articleid=0):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            return update_article(request,articleid)
    else:
        if articleid==0:
            form = EditForm()
            page_title=u'添加新文章'
        else:
            a = get_object_or_404(Article, aid=articleid)
            if request.user.username==a.authorname or in_editor_group(request.user):
                a_addon = AddonArticle.objects.get(aid=articleid)
                form = EditForm(initial={'title':a.title,
                    'typeid':a.typeid,
                    'u_text':a_addon.content})
                page_title=u'编辑-%s'%(a.title)
            else:
                return show_article(request,articleid,{'no_perm':True})
    return render_to_response('edit-article.html', {'form': form,
        'page_title': page_title,
        'aid':articleid},context_instance=RequestContext(request,processors=[custom_proc]))
        
@login_required
def delete_article(request,articleid):
    a = get_object_or_404(Article, aid=articleid)
    if request.user.username==a.authorname or in_editor_group(request.user):
        a.is_deleted=True
        a.save()
        return redirect(request,'/member/profile/%s/'%(a.authorname))#目前还没法在重定向的页面中提示删除成功，待完善
    else:
        return show_article(request,articleid,{'no_perm':True})
        
@login_required
def resume_article(request,articleid):
    '''可以与delete_article重构为同一个视图'''
    a = get_object_or_404(Article, aid=articleid)
    if in_admin_group(request.user):
        a.is_deleted=False
        a.save()
        return redirect(request,'/member/profile/%s/'%(a.authorname))
    else:
        raise Http404()

def update_article(request,articleid=0):
    typeid = request.POST.get('typeid', '')
    title = request.POST.get('title', '')
    u_text = request.POST.get('u_text', '')
    if articleid==0:
        a = Article(title=title,
            typeid=typeid,
            authorname=request.user.username)
        a.save()
        a_addon = AddonArticle(aid=a.aid,
            content=u_text,
            authorip=request.META['REMOTE_ADDR'])
        a_addon.save()
        sort_img(a.aid)
        return render_to_response('edit-article.html', {'form': EditForm(),
            'page_title': u'添加新文章',
            'result_aid':a.aid,
            'aid':articleid},context_instance=RequestContext(request,processors=[custom_proc]))#articleid是0时，表示添加新文章
    else:
        a = get_object_or_404(Article, aid=articleid)
        if request.user.username==a.authorname or in_editor_group(request.user):
            a.title = title
            a.typeid = typeid
            a_addon = AddonArticle.objects.get(aid=articleid)
            a_addon.content = u_text
            c=a_addon.content
            a.save()
            a_addon.save()
            sort_img(a.aid)
        else:
            return show_article(request,articleid,{'no_perm':True})
    return show_article(request,a.aid,{'has_edited':True})
    
def format_boolean(boolean_value):
    if boolean_value==u'True':
        return True
    elif boolean_value==u'False':
        return False
    else:
        return None
        