# -*-coding:utf-8 -*-
from PerfectCRM.Perfectcrm.crm import models
from django.shortcuts import render,redirect,HttpResponse
from django.forms import ValidationError
from django.utils.translation import ugettext as _
#from PerfectCRM.Perfectcrm.crm.admin import UserProfileAdmin
"""
enabled_admins={app_name：{tab_name：tab_obj}}
enabled_admins={app名字：{表一：表一对象，表二：表二对象}}
"""
enabled_admins = {}
class BaseAdmin(object):
    list_display = []
    list_filter = []
    list_per_page = 3
    search_fields = ['qq','name']
    ordering = None
    filter_horizontal = []
    actions = ["delete_selected_objs"]
    readonly_fields = ['qq','consultant','tags']
    #only_readonly = False
    readonly_table = False
    modelform_exclude_fields = []

    def delete_selected_objs(self,request,querysets):
        """
       #self: crm.CustomerAdmin
       :param arg1:arg1: <WSGIRequest: POST '/admin/crm/customer/'>,request
       :param arg2:<QuerySet [<Customer: 38399398@qq.com>
       :return:
       """
        print("delete_selected_objs",self,request,querysets)

        selected_ids = ','.join([str(i.id) for i in querysets])
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        if self.readonly_table:
            errors = {"readonly_table": "This table is readonly ,cannot be deleted or modified!" }
        else:
            errors ={}
        if request.POST.get("delete_confirm") == "yes":
            if not self.readonly_table:
                querysets.delete()
                return redirect("/kind_admin/%s/%s"%(app_name,table_name))

        return render(request,"kindadmin/table_objs_delete.html",{"admin_class":self,
                                                                  "objs":querysets,
                                                                  "app_name":app_name,
                                                                  "table_name":table_name,
                                                                  "selected_ids":selected_ids,
                                                                  "action":request._action,
                                                                  "errors":errors})

    delete_selected_objs.display_name = "删除多选数据"

    def default_form_validation(self):
        pass







class CustomerAdmin(BaseAdmin):

    list_display = ['id','qq','name','source','consult_course','consultant','status','date','enroll']
    list_filters = ['source','consultant','consult_course','status','date']
    search_fields = ['qq','name','consultant__name']
    #水平多选
    filter_horizontal = ['tags',]
    ordering = "id"
    _readonly_fields = False
    readonly_table = True



    #自定义一个新增展示的字段
    def enroll(self):
        if self.instance.status ==0:
            link_name = "报名新课程"
        else:
            link_name = "报名"
        erroll = '''<a href="/crm/customer/%s/enrollment">%s</a>'''% (self.instance.id,link_name)
        return erroll
    #为了在前端显示的字段是按照中文显示的
    enroll.display_name = "报名链接"

    def default_form_validation(self):
        content = self.cleaned_data.get("content")

        if len(content)<15:
            return ValidationError(
                    _('Field %(content)s length be >15'),
                    code='invalid',
                    params={'content': content},)
        #判断名字不能为空
        if not self.cleaned_data["name"]:
            self.add_error('name', "cannot be null")

    # #判断name不能为空kind_admin.py
    # def clean_name(self):
    #     print("name clean validation:", self.cleaned_data["name"])
    #     if not self.cleaned_data["name"]:
    #         self.add_error('name', "cannot be null")






class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['customer','consultant','date']
    list_filters = ['content','intention']
    #list_per_page=1

class UserProfileAdmin(BaseAdmin):
    list_display = ('email', 'name')
    readonly_fields = ('password')
    modelform_exclude_fields =["last_login"]

def register(model_class,admin_class=None):
    """
    :param model_class: models.Customer
    :param admin_class: CustomerAdmin
    :return:
    """
    #获取app_name
    app_name = model_class._meta.app_label

    #获取models里的表名
    table_name = model_class._meta.model_name

    # 判断app是否在enabled_admins中
    if app_name not in enabled_admins:
        enabled_admins[app_name] = {} #enabled_admins['crm'] ={}
    admin_class.model = model_class #绑定model对象和admin类 #model = models.Customer
    enabled_admins[app_name][table_name] = admin_class
    #enabled_admins['crm']['customerfollowup'] = CustomerFollowUpAdmin


class CourseRecordAdmin(BaseAdmin):
    list_display = ["from_class", "teacher", "outline", "day_num"]
    actions = ["initialization_course_record"]

    def initialization_course_record(self, request, queryset):
        # 只能选择一条一个班级的上课记录
        print("self,request,queryset:", self, request, queryset)
        if len(queryset) > 1:
            return HttpResponse("只能选择一条记录")
        # 找出这个班报名的学生数
        # print("queryset[0]:",queryset[0].from_class.enrollment_set.all())
        # (1062, "Duplicate entry '1-1' for key 'crm_studyrecord_student_id_course_record_id_24d12464_uniq'")
        # Cannot assign "<Customer: 190837349120>": "StudyRecord.student" must be a "Enrollment" instance.
        study_obj = []
        for enroll_obj in queryset[0].from_class.enrollment_set.all():
            # print("enroll_obj.customer",enroll_obj.customer)
            # models.StudyRecord.objects.get_or_create(student=enroll_obj,
            #                                   course_record=queryset[0],
            #                                   attendance =0,
            #                                   score=0)
            study_obj.append(models.StudyRecord(
                student=enroll_obj,
                course_record=queryset[0],
                attendance=0,
                score=0))
        try:
            models.StudyRecord.objects.bulk_create(study_obj)
            return redirect("/kind_admin/crm/studyrecord/")
        except Exception as e:
            return HttpResponse("有些数据已经有学习记录了")

    initialization_course_record.display_name = "初始化本节上课记录"


class StudyRecordAdmin(BaseAdmin):
    list_display = ["student", "course_record", "attendance", "score"]
    list_filter = ["course_record", "score", "attendance"]
    list_editable = ["score", "attendance"]


register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
register(models.UserProfile,UserProfileAdmin)
register(models.CourseRecord,CourseRecordAdmin)
register(models.StudyRecord,StudyRecordAdmin)










