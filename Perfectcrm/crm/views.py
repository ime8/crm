from django.shortcuts import render,HttpResponse,redirect
from PerfectCRM.Perfectcrm.crm.forms import EnrollmentForm,CustomerForm,PaymentFrom
from PerfectCRM.Perfectcrm.crm import models
from django.db import IntegrityError
import string,random
from django.core.cache import cache
from PerfectCRM.Perfectcrm.Perfectcrm import settings
import os
# Create your views here.
def index(request):
    return render(request,"index.html")

def customer_list(request):
    return render(request,"sales/customers.html")

def enrollment(request,customer_id):
    """销售填写报名信息"""
    #根据请求过来的customet_id获得该id的客户对象
    customer_obj = models.Customer.objects.get(id=customer_id)
    msgs={}
    if request.method == "POST":
        #把请求的数据放到表单里面
        enroll_form = EnrollmentForm(request.POST)
        #表单里面的是有效的
        if enroll_form.is_valid():
            msg='''请将此链接发送给客户进行填写:
                    http://localhost:8000/crm/customer/registration/{enroll_obj_id}/{random_str}'''
            try:
                print("cleaned_data",enroll_form.cleaned_data)
                #在enroll表单中加上前端的客户请求的值，因为客户的名称是从customer中获取，在enroll表中是没有的，会报错所以才在enroll中的customer添加他的值
                enroll_form.cleaned_data["customer"]= customer_obj
                #创建表单的值报名
                enroll_obj = models.Enrollment.objects.create(**enroll_form.cleaned_data)
                #报名生成的链接
                random_str = ''.join(random.sample(string.ascii_lowercase+string.digits,8))
                cache.set(enroll_obj.id,random_str,3600)
                msgs["msg"] = msg.format(enroll_obj_id=enroll_obj.id,random_str=random_str)
                #捕捉当用户已存在的错误
            except IntegrityError as e:
                #如果是改用户报名之前已经存在，那么报名的id就是要去customer表中找, 和enroll两个表中找关联的
                enroll_obj =models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                          enrolled_class_id = enroll_form.cleaned_data["enrolled_class"].id)
                if enroll_obj.contract_agreed:
                    return redirect("/crm/customer/%s/contract_review/"%enroll_obj.id)
                enroll_form.add_error("__all__","该用户已存在")
                random_str = ''.join(random.sample(string.ascii_lowercase+string.digits,8))
                cache.set(enroll_obj.id,random_str,3600)
                msgs["msg"] = msg.format(enroll_obj_id=enroll_obj.id,random_str=random_str)

    else:
        enroll_form = EnrollmentForm()
    return render(request,"sales/enrollment.html",{"enroll_form":enroll_form,
                                                   "customer_obj":customer_obj,
                                                   "msgs":msgs})

def stu_enrollment(request,enroll_id,random_str):
    """学生报名"""
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    #返回customer信息的时候的带他之前enroll的数据
    #customer_form = CustomerForm(instance=enroll_obj.customer)
    if cache.get(enroll_obj.id) == random_str:
        if request.method == "POST":

            if request.is_ajax():
                print("ajax post,",request.FILES)
                enroll_data_dir = "%s/%s"%(settings.ENROLLED_DATA,enroll_id)
                if not os.path.exists(enroll_data_dir):
                    os.makedirs(enroll_data_dir,exist_ok=True)
                for k,file_obj in request.FILES.items():
                    with open("%s/%s"%(enroll_data_dir,file_obj.name),"wb") as f:
                        for chunk in file_obj.chunks():
                            f.write(chunk)
                return HttpResponse("success")
            #更新customer的数据请求和库里面的
            customer_form = CustomerForm(request.POST,instance=enroll_obj.customer)
            #如果数据有效就保存
            if customer_form.is_valid():
                customer_form.save()
                enroll_obj.contract_agreed=True
                enroll_obj.save()
                return render(request,"sales/stuenrollment.html",{"status":1})
        else:
            #学员同意该合同
            if enroll_obj.contract_agreed:
                status=1
            else:
                status=0
            customer_form = CustomerForm(instance=enroll_obj.customer)

        return render(request,"sales/stuenrollment.html",{"customer_form":customer_form,
                                                          "enroll_obj":enroll_obj,
                                                          "status":status})
    else:
        return HttpResponse("url已经过期")


def contract_review(request,enroll_id):
    """销售审核合同"""
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    customer_form = CustomerForm(instance=enroll_obj.customer)

    return render(request,"sales/contract_review.html",{"enroll_obj":enroll_obj,
                                                        "customer_form":customer_form})

def payment(request,enroll_id):
    """学员缴费"""
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    customer_form = CustomerForm(instance=enroll_obj.customer)
    errors =[]
    if request.method == "POST":
        amount = request.POST.get("amount")
        print("amount",type(amount))
        if amount:
            try:
                amount = int(amount)
            except ValueError as e:
                errors.append("费用必须是数字")
            else:
                if amount >= 500:
                    payment_obj = models.Payment.objects.create(customer=enroll_obj.customer,
                                                                course=enroll_obj.enrolled_class.course,
                                                                amount=amount,
                                                                consultant=enroll_obj.consultant)
                    #更新合同的状态
                    enroll_obj.contract_approved = True
                    enroll_obj.save()
                    #更新报名的状态
                    enroll_obj.customer.status = 0
                    enroll_obj.customer.save()
                    return redirect("/kind_admin/crm/customer/")
                else:
                    errors.append("费用不能小于500元")
        else:
            errors.append("费用不能为空")
    return render(request,"sales/payment.html",{"enroll_obj":enroll_obj,
                                                "customer_form":customer_form,
                                                "errors":errors
                                                })