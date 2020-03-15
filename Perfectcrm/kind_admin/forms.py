from django.forms import forms,ModelForm
from PerfectCRM.Perfectcrm.crm import models
from django.forms import ValidationError
from django.utils.translation import ugettext as _

def creat_model_form(request,admin_class):


    def __new__(cls,*args,**kwargs):
        #super(CustomerForm,self).__new__(*args,**kwargs)
        # print("request.POST:",request.POST)
        for field_name,field_obj in cls.base_fields.items():
            #print(field_name,dir(field_obj))
            field_obj.widget.attrs['class'] = 'form-control'
            field_obj.widget.attrs['maxlength'] = getattr(field_obj,'max_length')if hasattr(field_obj,"max_length") else ''

            #判断表单字段如果是可读那就在前端加上disabled属性
            if not hasattr(admin_class,"is_add_form"):
                if field_name in admin_class.readonly_fields:
                    field_obj.widget.attrs["disabled"] = "disabled"

            #判断名字不能为空,加到form的claen_name中
            #判断admin_class里否有clean_name函数
            if hasattr(admin_class, 'clean_%s' % field_name):
                #获取clean_name函数
                field_clean_func = getattr(admin_class,"clean_%s" %field_name)
                #把clean_name函数添加到form的clean_field中
                setattr(cls, 'clean_%s'%field_name, field_clean_func)

        return ModelForm.__new__(cls)

    def defauct_clean(self):

        #from_web_datas = request.POST
        #print("from_web_datas",from_web_datas)
        list_error=[]
        if self.instance.id:
            for field in admin_class.readonly_fields:
                #在表单可读在数据库里的数据
                from_db_data = getattr(self.instance,field)
                #判断从数据库中取出的值是多对对的
                if hasattr(from_db_data,"select_related"):
                    #获取m2m多对多值的的对象
                    m2m_obj = getattr(from_db_data,"select_related")().select_related()
                    print("m2m_obj",m2m_obj)
                    #获取tags的值并切割出来
                    m2m_val = [i[0] for i in m2m_obj.values_list("id")]
                    #强转数据为集合为了与下面请求的数据比较
                    set_m2m_val = set(m2m_val)
                    print("set_m2m_val",set_m2m_val)
                    #多对多页面请求的值values值
                    set_m2m_vals_from_frontend = set([i.id for i in self.cleaned_data.get(field)])
                    print("set_m2m_vals_from_frontend",set_m2m_vals_from_frontend)
                    if set_m2m_val != set_m2m_vals_from_frontend:
                        self.add_error(field,"readonly field")
                    #这个就不执行下面语句了
                    continue

                #获取前端请求的数据
                from_web_data = self.cleaned_data.get(field,"")

                print("form_db_data:",field,from_db_data,from_web_data)

                if from_db_data!= from_web_data:
                    list_error.append(ValidationError(
                        _('Field %(field)s is readonly data should be %(value)s'),
                        code='invalid',
                        params={'field': field,'value':from_db_data},
                    ))




        if hasattr(admin_class,'default_form_validation'):
            default_form_error_info =admin_class.default_form_validation(self)
            if default_form_error_info:
                list_error.append(default_form_error_info)




        if list_error:
            raise ValidationError(list_error)






    class Meta:
        model = admin_class.model
        fields = "__all__"
        #不显示form的字段用exclude
        exclude =admin_class.modelform_exclude_fields 

    attr = {"Meta":Meta}
    _model_form_class = type("DynamicModelForm",(ModelForm,),attr)
    setattr(_model_form_class,'__new__',__new__)
    setattr(_model_form_class,'clean',defauct_clean)
    return _model_form_class




