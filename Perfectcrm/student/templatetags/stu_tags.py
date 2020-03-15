# -*- coding:utf-8 -*-
#date: 2019/07/28 23:05
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from django.db.models import Sum
from django.core.exceptions import FieldDoesNotExist
register = template.Library()
@register.simple_tag
def get_score(enroll_obj):
    #找到这个用户的课程的所有学习记录，这个学习记录的课程在上课记录里面是有的
    study_recore = enroll_obj.studyrecord_set.all().filter(course_record__from_class_id=enroll_obj.enrolled_class.id)
    return study_recore.aggregate(Sum('score'))