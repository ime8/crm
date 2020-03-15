# -*- coding:utf-8 -*-
#date: 2019/07/28 23:05
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from django.core.exceptions import FieldDoesNotExist
register = template.Library()
@register.simple_tag
def render_app_name(admin_class):
    """
h
    :param admin_class: CustomerFollowUpAdmin
    :return: 获取表的中文名称
    """
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):
    """

    :param admin_class: CustomerFollowUpAdmin
    :return: 返回表里的所有数据
    """
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_raw(obj,admin_class,request):
    """

    :param obj: admin_class.model.objects.all(),在前端已经一个一个的类数据循环
    :param admin_class: CustomerAdmin
    :return:对应字段的值
    """
    raw_ele = ""
    for index,column in enumerate(admin_class.list_display):
        #获取该类内指定字段的信息
        try:
            field_obj = obj._meta.get_field(column)
            if field_obj.choices:
                #获取字段choices里的中文值
                column_data = getattr(obj,"get_%s_display" %column)()
            else:
                column_data = getattr(obj,column)

            #print("type(column_date)类型:",column,type(column).__name__)
            if type(column_data).__name__ == 'datetime':
                column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")

            if index==0:
                column_data = "<a href='{request_path}{colum_id}/change/'>{data}</a>".format(request_path=request.path,
                                                                                            colum_id=obj.id,
                                                                                            data=column_data)
        except FieldDoesNotExist as e:

            hasattr(admin_class,column)
            #在admin加instance=obj,为了能够找到这笔数据的id值
            admin_class.instance =obj

            column_func = getattr(admin_class,column)

            column_data = column_func()

        raw_ele += "<td>%s</td>" % column_data


    return mark_safe(raw_ele)

@register.simple_tag
def render_page_ele(loop_counter,query_sets,filter_condtions):
    """分页显示"""
    sel_ele =""
    for k,v in filter_condtions.items():
        sel_ele+="&%s=%s"%(k,v)

    #query_sets.number表示当前页
    if abs(query_sets.number - loop_counter) <= 1:
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' %(ele_class,loop_counter,sel_ele,loop_counter)

        return mark_safe(ele)
    return ''

@register.simple_tag
def build_paginator(query_sets,filter_condtions,previous_orderkey,search_value):
    #"""页面分页中间会是....显示"""
    """
    :param query_sets: 页面值的对象
    :param filter_condtions: 请求数据的dict
    :return: 返回分页
    """
    sel_ele = ""
    page_ele = ""
    for k ,v in filter_condtions.items():
        sel_ele+="&{0}={1}".format(k,v)
    added_bot_ele = False
    for page_num in query_sets.paginator.page_range:
        #print("page_num",page_num)
        #前量页和最后两页和当前页的前后两页显示，其他的用....显示
        if page_num<3 or page_num>query_sets.paginator.num_pages-2 or abs(query_sets.number-page_num)<=2:
            ele_class =""
            added_bot_ele = False
            if page_num == query_sets.number:
                ele_class ="active"
            page_ele+='''<li class="%s"><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>'''%(ele_class,page_num,sel_ele,previous_orderkey,search_value,page_num)

        else:
            if not added_bot_ele:
                page_ele+='''<li><a>....</a><li>'''
                added_bot_ele =True

    return mark_safe(page_ele)


@register.simple_tag
def render_filter_ele(condtion,admin_class,filter_condtions):
    #后台返回筛选框里面的值
    """
    :param condtion: 需要过滤的字段名
    :param admin_class: 比如Customer
    :param filter_condtions: 前端请求数据的json
    :return:
    """
    select_ele = '''<select class="form-control" name='{condtion_name}'><option value=''>----</option>'''
    filed_obj = admin_class.model._meta.get_field(condtion)
    #判断如果是choices类型
    if filed_obj.choices:
        selected=''
        for choice_item in filed_obj.choices:
            print("choice", choice_item, filter_condtions.get(condtion), type(filter_condtions.get(condtion)))
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"

            select_ele+='''<option value='%s' %s>%s</option>'''%(choice_item[0],selected,choice_item[1])
            selected=''
    #判断如果是属于ForeignKey类型的时候
    if type(filed_obj).__name__ == 'ForeignKey':
        selected = ''
        for choice_item in filed_obj.get_choices()[1:]:
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected ="selected"


            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''
    #判断是属于日期类型的时候
    if type(filed_obj).__name__ in ["DateTimeField","DateField"]:
        selected =''
        today_ele = datetime.now().date()
        date_eles = []
        date_eles.append(("今天",today_ele))
        date_eles.append(("7天",today_ele-timedelta(days=7)))
        date_eles.append(("本月",today_ele.replace(day=1)))
        date_eles.append(("半年",today_ele-timedelta(days=180)))
        date_eles.append(("一年",today_ele.replace(month=1,day=1)))
        for dateEle in date_eles:
            select_ele += '''<option value='%s'%s>%s</option>''' % (dateEle[1], selected,dateEle[0])

        condtion_name = "%s__gte"%(condtion)

    else:
        condtion_name = condtion

    select_ele+="<select/>"

    select_ele= select_ele.format(condtion_name=condtion_name)

    return mark_safe(select_ele)


@register.simple_tag
def build_reverse_order(column,order_key,filter_condtions,admin_class):
    """页面排序展示交换反转"""
    sel_ele = ""
    for k, v in filter_condtions.items():
        sel_ele+= "&%s=%s" %(k, v)

    ele = '''<th><a href="?{sel_ele}&o={order_key}">{column}</a>
                {icon}
            </th>'''

    if order_key:

        if order_key.startswith("-"):
            icon = '''<span class="glyphicon glyphicon-triangle-top" aria-hidden="true"></span>'''
        else:
            icon = '''<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>'''

        if order_key.strip("-") == column or order_key == column:
            order_key=order_key

        else:
            order_key=column
            icon = ""
    else:
        order_key = column
        icon=""

    try:
        column_verbose_name = admin_class.model._meta.get_field(column).verbose_name
        ele = ele.format(order_key=order_key, column=column_verbose_name, icon=icon, sel_ele=sel_ele)

    except FieldDoesNotExist as e:
        if hasattr(admin_class,column):
            column_func = getattr(admin_class,column)
            column_verbose_name = column_func.display_name
            ele = '''<th><a href="javascript:void(0);">{column}</th>'''
            ele = ele.format(column=column_verbose_name)

    return mark_safe(ele)

@register.simple_tag
def get_m2m_choose_data(admin_class,filed_form,filed_obj):
    #获取所有待选的数据
    """
    :param admin_class: Customer
    :param filed_form: 表单
    :param filed_obj :表单List
    :return: 返回没有在右边表单框的数据
    """
    field_obj = getattr(admin_class.model,filed_form.name)
    #表结构对象的某个字段
    all_obj_list =field_obj.rel.model.objects.all()
    #单条数据的对象中的某个字段
    #obj_instance_field = getattr(filed_obj.instance,filed_form.name)
    if filed_obj.instance.id:
        obj_instance_field = getattr(filed_obj.instance, filed_form.name)
        seleced_obj_list = obj_instance_field.all()
        standby_obj_list =[]
        for all_obj in all_obj_list:
            if all_obj not in seleced_obj_list:
                standby_obj_list.append(all_obj)
        return standby_obj_list
    else:
        return all_obj_list


@register.simple_tag
def get_m2m_selected_obj(filed_form,form_obj):
    """
    :param filed_form: 表单
    :param form_obj: 表单list
    :return:
    """
    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance,filed_form.name)
        return field_obj.all()


@register.simple_tag
def recursive_related_objs_lookup(objs):
    #model_name = objs[0]._meta.model_namme

    #m = models.Customer.objects.get(id=20)
    ul_ele = "<ul>"
    for obj in objs:
        li_ele = '''<li>%s:%s</li>'''%(obj._meta.verbose_name,obj.__str__().strip("<>"))
        ul_ele +=li_ele

        #many_to_many的对象
        #print("------- obj._meta.local_many_to_many", obj._meta.local_many_to_many)
        for m2m_field in obj._meta.local_many_to_many: #把所有跟这个对象直接关联的m2m字段取出来
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj,m2m_field.name) #getattr(customer,'tags')
            for o in m2m_field_obj.select_related(): #customer.tags.select_related()
                li_ele ='''<li>%s:%s</li>''' %(m2m_field.verbose_name,o.__str__().strip("<>"))
                sub_ul_ele+=li_ele
            sub_ul_ele +="</ul>"
            ul_ele +=sub_ul_ele #最后跟最外层的ul相拼接
        #一对一的
        #red =m._meta.related_objects
        for related_obj in obj._meta.related_objects:
            #red[1].__repr__()
            if 'ManyToManyRel' in related_obj.__repr__():
                #hasattr(m,red[0].get_accessor_name())
                if hasattr(obj,related_obj.get_accessor_name()):
                    #getattr(m,red[0].get_accessor_name())
                    accessor_obj = getattr(obj,related_obj.get_accessor_name())
                    #上面的accessor_obj相当于customer.enrollment_set
                    if hasattr(accessor_obj,'select_related'): #select_related()==all()
                        target_objs = accessor_obj.select_related() # .filter(**filter_coditions)
                        # target_objs 相当于 customer.enrollment_set.all()
                        sub_ul_ele = "<ul style='color:red'>"
                        for o in target_objs:
                            li_ele = '''<li> %s:%s </li>''' %(o._.meta.verbose_name,o.__str__().strip("<>"))
                            sub_ul_ele+=li_ele
                        sub_ul_ele+="</ul>"
                        ul_ele+=sub_ul_ele
            elif hasattr(obj,related_obj.get_accessor_name()): ## hassattr(customer,'enrollment_set')
                accessor_obj = getattr(obj,related_obj.get_accessor_name())
                # 上面accessor_obj 相当于 customer.enrollment_set
                if hasattr(accessor_obj,'select_related'): #select_related() == all()
                    target_objs = accessor_obj.select_related() ##.filter(**filter_coditions)
                    # target_objs 相当于 customer.enrollment_set.all()

                else:
                    print("one to one i guess:",accessor_obj)
                    target_objs = accessor_obj
                if len(target_objs) >0:
                    nodes = recursive_related_objs_lookup(target_objs)
                    ul_ele += nodes
    ul_ele+="</ul>"
    return ul_ele

@register.simple_tag
def display_obj_related(objs):
    #objs = [obj,]
    if objs:
        model_class = objs[0]._meta.model #models.Customer
        model_name = objs[0]._meta.model_name

        return mark_safe(recursive_related_objs_lookup(objs))

@register.simple_tag
def get_action_verbose_name(admin_class,action):
    action_func = getattr(admin_class,action)
    return action_func.display_name if hasattr(action_func,"display_name") else action









