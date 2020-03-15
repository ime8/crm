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
from PerfectCRM.Perfectcrm.student import views

urlpatterns = [
    #课程详情
    url(r'^$',views.stu_my_class,name='stu_my_class'),
    #课程学习记录
    url(r'mycourse/(\d+)$',views.mycourse,name='mycourse'),
    #提交作业
    url(r'my_homework/(\d+)$',views.my_homework,name='my_homework'),


]
