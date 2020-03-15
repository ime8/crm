# -*- coding:utf-8 -*-
#date: 2019/07/28 23:05
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from django.core.exceptions import FieldDoesNotExist
register = template.Library()
@register.simple_tag
def render_enroll_contract(enroll_obj):
    return enroll_obj.enrolled_class.contract.template.format(cunstomer_qq=enroll_obj.customer.qq,
                                                     enroll_course=enroll_obj.enrolled_class.course)
