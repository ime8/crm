#date:2019/09/01
from django.forms import ModelForm
from PerfectCRM.Perfectcrm.crm import models

class CustomerForm(ModelForm):
    """客户表单"""
    def __new__(cls,*args,**kwargs):
        #super(CustomerForm,self).__new__(*args,**kwargs)
        # print("request.POST:",request.POST)
      #表名，表对象值
        for field_name,field_obj in cls.base_fields.items():
            #print(field_name,dir(field_obj))
            #给表输入框添加class
            field_obj.widget.attrs['class'] = 'form-control'
            if field_name in cls.Meta.readonly_fields:
                #添加disabled属性
                field_obj.widget.attrs['disabled'] = 'disabled'

        return ModelForm.__new__(cls)


    def clean_qq(self):
        #不能修改的值取数据库中的值和页面的值相比较
        if self.instance.qq != self.cleaned_data["qq"]:
            self.add_error("qq","小样竟敢黑我小瞧我了")
        else:
            return self.instance.qq

    def clean_source(self):
        #不能修改的值取数据库中的值和页面的值相比较
        if self.instance.source != self.cleaned_data["source"]:
            #添加表单错误信息
            self.add_error("source","小样竟敢黑我小瞧我了")
        else:
            return self.instance.source

    def clean_consultant(self):
        #不能修改的值取数据库中的值和页面的值相比较
        if self.instance.consultant != self.cleaned_data["consultant"]:
            self.add_error("consultant","小样竟敢黑我小瞧我了")
        else:
            return self.instance.consultant
    def clean_name(self):
        if not self.cleaned_data["name"]:
            self.add_error("name","name不能为空")
        else:
            return self.cleaned_data["name"]



    class Meta:
        model =models.Customer
        fields ='__all__'
        #不在前端显示
        exclude =["tags","content","memo","status","referral_from","consult_course"]
        #只读属性
        readonly_fields =["qq","consultant","source"]

class EnrollmentForm(ModelForm):
    """报名表单"""
    def __new__(cls,*args,**kwargs):
        #super(CustomerForm,self).__new__(*args,**kwargs)
        # print("request.POST:",request.POST)
      #表名，表对象值
        for field_name,field_obj in cls.base_fields.items():
            #print(field_name,dir(field_obj))
            #给表输入框添加class
            field_obj.widget.attrs['class'] = 'form-control'

        return ModelForm.__new__(cls)


    class Meta:
        model = models.Enrollment
       #表单展示的字段
        fields = ["enrolled_class","consultant"]

class PaymentFrom(ModelForm):
    """学员缴费页面"""
    def __next__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
        return ModelForm.__new__(cls)
    class Meta:
        model = models.Payment
        fields ="__all__"


