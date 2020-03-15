# -*-coding:utf-8 -*-
#date: 2019-08-3 15:35
#Q用法


from django.db.models import Q

def table_filter(request,admin_class):
    """进行条件过滤并返回过滤后的数据"""

    filter_conditions = {}
    for column in admin_class.list_display:
        if hasattr(admin_class,column):
            admin_class.model.column =""
    for k,v in request.GET.items():
        kitem =['page','o','_q']
        if k in kitem:
            continue
        if v:
            filter_conditions[k]=v
    print("filter_conditions:",filter_conditions)
    print("admin_class.model.objects.filter(**filter_conditions)",admin_class.model.objects.filter(**filter_conditions))
    return admin_class.model.objects.filter(**filter_conditions).order_by("-%s"% admin_class.ordering if admin_class.ordering else "-id") \
        ,filter_conditions

def table_order(request,objs,admin_class):
    """判断请求过来是否有o字段，有就排序"""
    orderby_key = request.GET.get("o")

    if orderby_key:
        print("orderby_key_obj:",objs)

        objs=objs.order_by(orderby_key)

        #print("objs.order_by(orderby_key):", objs.order_by(orderby_key))
        if orderby_key.startswith("-"):
            orderby_key=orderby_key.strip("-")
        else:
            orderby_key = ("-%s")%orderby_key
    return objs,orderby_key


def table_search(request,admin_class,objs):
    """
    多条件搜索功能
    :param request: 请求的
    :param admin_class: Customer
    :param objs: 筛选过后的对象
    :return:
    """
    search_value = request.GET.get("_q","")
    if search_value:
        con = Q()
        con.connector="OR"
        for column in admin_class.search_fields:
            con.children.append(('%s__contains'%column,search_value))

        ele = objs.filter(con)
    else:
        ele =objs

    return ele


