from django.contrib import admin

# Register your models here.
from PerfectCRM.Perfectcrm.crm import models
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.shortcuts import render,redirect,HttpResponse


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','qq','source','consultant','content','status','date')
    list_filters = ('source','consultant','date')
    search_fields = ('qq','name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)

    actions = ["test_action"]
    def test_action(self,arg1,arg2):
        """
        #self: crm.CustomerAdmin
        :param arg1:arg1: <WSGIRequest: POST '/admin/crm/customer/'>,request
        :param arg2:<QuerySet [<Customer: 38399398@qq.com>
        :return:
        """
        print('test action:')
        print('self:',self)
        print('arg1:',arg1)
        print('arg2:',arg2)


# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user','name')



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile

        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','stu_account')}),
        ('Permissions', {'fields': ('is_admin','roles','is_active','groups','user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ("roles","groups","user_permissions")

# Now register the new UserAdmin...
admin.site.register (models.UserProfile, UserProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)



class CourseRecordAdmin(admin.ModelAdmin):

    list_display =["from_class","teacher","outline","day_num"]
    actions = ["initialization_course_record"]
    def initialization_course_record(self,request,queryset):
        #只能选择一条一个班级的上课记录
        print("self,request,queryset:",self,request,queryset)
        if len(queryset)>1:
            return HttpResponse("只能选择一条记录")
        #找出这个班报名的学生数
        #print("queryset[0]:",queryset[0].from_class.enrollment_set.all())
        #(1062, "Duplicate entry '1-1' for key 'crm_studyrecord_student_id_course_record_id_24d12464_uniq'")
        #Cannot assign "<Customer: 190837349120>": "StudyRecord.student" must be a "Enrollment" instance.
        study_obj=[]
        for enroll_obj in queryset[0].from_class.enrollment_set.all():
            #print("enroll_obj.customer",enroll_obj.customer)
            #如果有了就查询没有就创建，不然会报唯一性错误
            #这个是每一条一条的提交事物，如果数据太大的话性能会比较差
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
            #bulk_create可以创建很多个但是这个事务是提交的如50条，50条失败
            models.StudyRecord.objects.bulk_create(study_obj)
            return redirect("/admin/crm/studyrecord/")
        except Exception as e:
            return HttpResponse("有些数据已经有学习记录了")
    #actions函数名显示中文名short_description
    initialization_course_record.short_description = "初始化本节上课记录"

class StudyRecordAdmin(admin.ModelAdmin):
    list_display=["student","course_record","attendance","score"]
    list_filter = ["course_record","score","attendance"]
    #可编辑的
    list_editable = ["score","attendance"]

class LevelAdmin(admin.ModelAdmin):
    list_display = ["name"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

class VideoAdmin(admin.ModelAdmin):
    list_display = ["level","category","title"]

class DirectionAdmin(admin.ModelAdmin):
    list_display = ["name"]


#在admin后台注册某个字段
admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Enrollment)
admin.site.register(models.Course)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord,CourseRecordAdmin)
admin.site.register(models.Branch)
admin.site.register(models.Role)
admin.site.register(models.Payment)
admin.site.register(models.StudyRecord,StudyRecordAdmin)
admin.site.register(models.Tag)
#admin.site.register(models.UserProfile,UserProfileAdmin)
admin.site.register(models.Menu)
admin.site.register(models.ContractTemplate)

admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.Level,LevelAdmin)
admin.site.register(models.Video,VideoAdmin)
admin.site.register(models.Direction,DirectionAdmin)



