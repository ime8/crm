from django.shortcuts import render,redirect
from PerfectCRM.Perfectcrm.kind_admin import kind_admin
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from PerfectCRM.Perfectcrm.kind_admin.utils import table_filter,table_order,table_search
from PerfectCRM.Perfectcrm.kind_admin.forms import creat_model_form
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def index(request):

    return render(request,"kindadmin/table_index.html",{"table_list":kind_admin.enabled_admins})
@login_required
def display_table_objs(request,app_name,table_name):
    """搜索、分页、排序页面"""
    print("-->",app_name,table_name)
    #models_module = importlib.import_module('%s.models'%(app_name))
    #model_obj = getattr(models_module,table_name)
    admin_class = kind_admin.enabled_admins[app_name][table_name]
    #admin_class = king_admin.enabled_admins[crm][userprofile]
    if request.method == 'POST': #action来了
        action = request.POST.get("action")
        selected_ids = request.POST.get("selected_ids")
        if selected_ids:#filter
            selected_ids = admin_class.model.objects.filter(id__in=(selected_ids.split(',')))
        else:
            raise KeyError("no object select")
        if hasattr(admin_class,action):
            #获取admin_class里面的delete_selected_obj函数
            action_func = getattr(admin_class,action)
            #在请求里面手动添加action为在删除提交时有action
            request._action = action
            #返回调用
            return action_func(admin_class,request,selected_ids)



    #object_list = admin_class.model.objects.all()
    #过滤
    object_list,filter_condtions = table_filter(request,admin_class)

    #多条件搜索功能

    object_list = table_search(request,admin_class,object_list)
    #排序过后的数据
    object_list,order_key = table_order(request,object_list,admin_class)

    paginator = Paginator(object_list, admin_class.list_per_page) # Show 25 contacts per page
    print("paginator------",paginator)
    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1) ##这个是对你的分页的数据进行取值
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)
    print("query_sets------------",query_sets)
    return render(request,"kindadmin/table_objs.html",{"admin_class":admin_class,
                                                        "query_sets":query_sets,
                                                        "filter_condtions":filter_condtions,
                                                       "order_key":order_key,
                                                       "previous_orderkey":request.GET.get("o",""),
                                                       "search_value":request.GET.get("_q","")})
@login_required
def table_objs_change(request,app_name,table_name,obj_id):
    """修改更新信息页面"""

    admin_class = kind_admin.enabled_admins[app_name][table_name]
    model_form_class = creat_model_form(request,admin_class)

    obj = admin_class.model.objects.get(id=obj_id)


    if request.method == "POST":
        print("修改更新信息页面",request.POST)
        form_obj = model_form_class(request.POST,instance=obj) #更新
        print("-------------------request.POST,instance=obj---------------------")
        #判断更新的值是否合法
        if form_obj.is_valid():

            form_obj.save()
    else:
        form_obj = model_form_class(instance=obj)


    return render(request,"kindadmin/table_objs_change.html",{"form_obj":form_obj,
                                                              "admin_class":admin_class,
                                                              "app_name":app_name,
                                                              "table_name":table_name})

@login_required
def table_objs_add(request,app_name,table_name):
    """增加信息页面"""

    admin_class = kind_admin.enabled_admins[app_name][table_name]
    model_form_class = creat_model_form(request, admin_class)
    admin_class.is_add_form = True
    #admin_class.only_readonly = True
    if request.method == 'POST':
        form_obj = model_form_class(request.POST) #新增
        if form_obj.is_valid():
            form_obj.save()
        return redirect(request.path.replace("/add/","/"))

    else:
        form_obj = model_form_class()


    return render(request,"kindadmin/table_objs_add.html",{"form_obj":form_obj,
                                                           "admin_class":admin_class})

@login_required
def table_objs_delete(request,app_name,table_name,obj_id):
    """
    #删除数据
    :param request:
    :param app_name: crm
    :param table_name: Costomer
    :param obj_id: Costomer.id
    :return:
    """
    admin_class = kind_admin.enabled_admins[app_name][table_name]
    obj = admin_class.model.objects.get(id=obj_id)
    if admin_class.readonly_table:
        errors = {"readonly_table": "table is readonly ,obj [%s] cannot be deleted" % obj}
    else:
        errors = {}

    if request.method == "POST":
        if not admin_class.readonly_table:
            obj.delete()
            return redirect("/kind_admin/%s/%s/" %(app_name,table_name))
    objs =[obj,]
    return render(request,"kindadmin/table_objs_delete.html",{"admin_class":admin_class,
                                                              "objs":objs,
                                                              "app_name":app_name,
                                                              "table_name":table_name,
                                                              "obj_id":obj_id,
                                                              "errors": errors,})
@login_required
def password_reset(request,app_name,table_name,obj_id):

    admin_class = kind_admin.enabled_admins[app_name][table_name]
    obj = admin_class.model.objects.get(id=obj_id)
    error = {}
    if request.method == "POST":
        print("password_request:",request.POST)
        #09XpuPq'], 'password1': ['123456'], 'password2': ['123456']}>

        _password1 = request.POST.get("password1")
        _password2 = request.POST.get("password2")

        if len(_password1)<5 or _password1 is None or _password2 is None:
            error={"password":"密码为空或者密码长度小于5"}

        elif _password1 == _password2:

            obj.set_password(_password1)
            obj.save()
            return redirect(request.path.rstrip("passworld/"))
        else:
            error={"password":"two password no some"}

    return render(request,"kindadmin/password_reset.html",{"obj":obj,
                                                           "error":error})

