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
from PerfectCRM.Perfectcrm.kind_admin import views

urlpatterns = [
    url(r'^$',views.index,name='table_index'),
    url(r'^(\w+)/(\w+)/$',views.display_table_objs,name='table_objs'),
    #修改数据
    url(r'^(\w+)/(\w+)/(\d+)/change/$',views.table_objs_change,name='table_objs_change'),
    #新增数据
    url(r'^(\w+)/(\w+)/add/$', views.table_objs_add, name='table_objs_add'),
    #删除数据
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_objs_delete, name='table_objs_delete'),
    #修改密码的url
    url(r'^(\w+)/(\w+)/(\d+)/change/password',views.password_reset,name='password_reset'),

]
