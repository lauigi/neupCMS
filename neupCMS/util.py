#-*- coding:utf-8 -*-
import re
from articles.models import AddonArticle
from upload.models import ImageUpload
from PIL import Image,ImageFilter
from django.core.files import File
from tempfile import NamedTemporaryFile


def img_from_content(aid):
    a_addon=AddonArticle.objects.get(aid=aid)
    pattern = re.compile(ur'src="(?P<pre>/media/)(?P<tail>images/[\d]{4}/[\d]{2}/[\d]{2}/[\d]{14,15}\.)([\w]{3,4})')
    s=pattern.pattern
    t=a_addon.content
    img_list=[]
    match = pattern.findall(t)
    for item in match:
        img_list.append('thumb/'+item[1]+'png')
    return img_list
    
def sort_img(articleid):
    img_list=img_from_content(articleid)
    for thumb_path in img_list:
        try:
            ImageUpload.objects.filter(thumb_path=thumb_path).update(aid=articleid)
        except ImageUpload.DoesNotExist:
            pass

def make_thumb(img,width = 350,height=250):
    pixbuf = Image.open(img)
    target_delta = float(width)/height
    delta=pixbuf.size[0]/pixbuf.size[1]
    pixbuf.thumbnail((width, height), Image.ANTIALIAS)
    pixbuf=dropShadow(pixbuf)
    temp_img_file=NamedTemporaryFile()
    pixbuf.save(temp_img_file,"png")
    thumb_img=File(temp_img_file)
    return thumb_img

def dropShadow( image, back_width=350,back_height=250,offset=(5,5), background=(0,0,0,0),
        shadow=(0,0,0,100), border=8, iterations=3):
    """
    把图像放在一个作了高斯模糊的背景上
    image       - 要放在背景上的原始图像
    offset      - 阴影相对图像的偏移，用(x,y)表示，可以为正数或者负数
    background - 背景色
    shadow      - 阴影色
    border      - 图像边框，必须足够用来制作阴影模糊
    iterations - 过滤器处理次数，次数越多越模糊，当然处理过程也越慢
    """
    image=image.convert(mode='RGBA')
    # 创建背景块
    totalWidth = image.size[0] + abs(offset[0]) + 2*border
    totalHeight = image.size[1] + abs(offset[1]) + 2*border
    back = Image.new(image.mode, (totalWidth, totalHeight), background)
 
    # 放置阴影块，考虑图像偏移
    shadowLeft = border + max(offset[0], 0)
    shadowTop = border + max(offset[1], 0)
    back.paste(shadow, [shadowLeft, shadowTop, shadowLeft + image.size[0],
        shadowTop + image.size[1]] )
 
    # 处理阴影的边缘模糊
    n = 0
    while n < iterations:
        back = back.filter(ImageFilter.BLUR)
        n += 1
 
    # 把图像粘贴到背景上
    imageLeft = border - min(offset[0], 0)
    imageTop = border - min(offset[1], 0)
    back.paste(image, (imageLeft, imageTop))
    thumb = Image.new(image.mode, (back_width, back_height), background)
    thumb.paste(back, ((back_width-totalWidth)/2, (back_height-totalHeight)/2))
 
    return thumb
    
