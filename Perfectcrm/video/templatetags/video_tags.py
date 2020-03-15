# -*- coding:utf-8 -*-
#date: 2019/07/28 23:05
from django import template
from django.utils.safestring import mark_safe

from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from django.db.models import Sum
from django.core.exceptions import FieldDoesNotExist
from django.urls import reverse
register = template.Library()
@register.simple_tag
def catagory_tag(catagory,arg_dic):
    """
    等级
    :param catagory:
    :param arg_dic:
    :return:
    """
    url = reverse("table_video",kwargs={"level_id":arg_dic.get("level_id"),"category_id":catagory.id})
    if str(catagory.id) == arg_dic.get("category_id"):

        tag = '''<a href="%s" style="color:red">%s</a>'''%(url,catagory.name)
        return mark_safe(tag)
    else:
        tag = '''<a href="%s">%s</a>'''%(url,catagory.name)
        return mark_safe(tag)

@register.simple_tag
def level_tag(level,arg_dic):
    url = reverse("table_video",kwargs={"level_id":level.id,"category_id":arg_dic.get("category_id")})

    if str(level.id) == arg_dic.get("level_id"):
        tag = '''<a href="%s" style="color:red">%s</a>'''%(url,level.name)
        return mark_safe(tag)
    else:
        tag = '''<a href="%s">%s</a>'''%(url,level.name)
        return mark_safe(tag)

@register.simple_tag
def tag_all(arg_dic,key):
    if key == "catagory_id":
        url = reverse("table_video", kwargs={"level_id": arg_dic.get("level_id"), "category_id":0})
    elif key == "level_id":
        url = reverse("table_video", kwargs={"level_id":0 , "category_id":arg_dic.get("category_id")})

    tag = '''<a href="%s">全部</a>'''%(url,)
    return mark_safe(tag)


#三个条件
@register.simple_tag
def direction_tag(direction,arg_dic):
    """
    方向
    :param catagory:
    :param arg_dic:
    :return:
    """
    url = reverse("table_video2",kwargs={"dr_id":direction.id,"level_id":arg_dic.get("level_id"),"category_id":arg_dic.get("category_id")})
    if str(direction.id) == arg_dic.get("dr_id"):

        tag = '''<a href="%s" style="color:red">%s</a>'''%(url,direction.name)
        return mark_safe(tag)
    else:
        tag = '''<a href="%s">%s</a>'''%(url,direction.name)
        return mark_safe(tag)

@register.simple_tag
def three_catagory_tag(catagory,arg_dic):
    """
    等级
    :param catagory:
    :param arg_dic:
    :return:
    """
    url = reverse("table_video2",kwargs={"dr_id":arg_dic.get("dr_id"),"level_id":arg_dic.get("level_id"),"category_id":catagory.id})
    if str(catagory.id) == arg_dic.get("category_id"):

        tag = '''<a href="%s" style="color:red">%s</a>'''%(url,catagory.name)
        return mark_safe(tag)
    else:
        tag = '''<a href="%s">%s</a>'''%(url,catagory.name)
        return mark_safe(tag)


@register.simple_tag
def three_level_tag(level,arg_dic):
    url = reverse("table_video2",kwargs={"dr_id":arg_dic.get("dr_id"),"level_id":level.id,"category_id":arg_dic.get("category_id")})

    if str(level.id) == arg_dic.get("level_id"):
        tag = '''<a href="%s" style="color:red">%s</a>'''%(url,level.name)
        return mark_safe(tag)
    else:
        tag = '''<a href="%s">%s</a>'''%(url,level.name)
        return mark_safe(tag)

@register.simple_tag
def three_tag_all(arg_dic,key):
    if key == "dr_id":
        url = reverse("table_video2", kwargs={"dr_id":0,"level_id": arg_dic.get("level_id"), "category_id": arg_dic.get("category_id")})
    elif key == "category_id":#category_id
        url = reverse("table_video2", kwargs={"dr_id":arg_dic.get("dr_id"),"level_id": arg_dic.get("level_id"), "category_id":0})
    elif key == "level_id":
        url = reverse("table_video2", kwargs={"dr_id":arg_dic.get("dr_id"),"level_id":0 , "category_id":arg_dic.get("category_id")})
    else:
        url=""
    if arg_dic.get(key) == "0":
        tag = '''<a href="%s" style="color:red">全部</a>'''%(url,)
    else:
        tag = '''<a href="%s">全部</a>''' % (url,)

    return mark_safe(tag)







