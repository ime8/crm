"""Perfectcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from PerfectCRM.Perfectcrm.crm import views

urlpatterns = [
    url(r'^$',views.index,name='sales_index'),
    url(r'^customers/$',views.customer_list,name="customer_list"),
    url(r'^customer/(\d+)/enrollment/$', views.enrollment, name="enrollment"),
    url(r'^customer/registration/(\d+)/(\w+)$', views.stu_enrollment, name="stu_enrollment"),
    #审核合同
    url(r'^customer/(\d+)/contract_review/$', views.contract_review, name="contract_review"),
    #缴费
    url(r'^customer/(\d+)/payment/$', views.payment, name="payment"),

]
