from django.shortcuts import render,HttpResponse
from PerfectCRM.Perfectcrm.crm import models
# Create your views here.
def video(request,*args,**kwargs):
    contain = {}
    print(kwargs)
    for k,v in kwargs.items():
        if v == '0':
            contain = {}
        else:
            contain[k]=v


    catagory_list = models.Category.objects.all()
    level_list = models.Level.objects.all()
    results = models.Video.objects.filter(**contain)
    print("results",results)
    return render(request,"video/video.html",{"catagory_list":catagory_list,
                                              "level_list":level_list,
                                              "results":results,
                                              "kwargs":kwargs,})


def video2(request,*args,**kwargs):
    #0-0-0.html
    #1-0-0.html
    #1-1-0.html
    dr_id = kwargs.get("dr_id")
    cg_id = kwargs.get("category_id")
    lv_id = kwargs.get("level_id")
    condition = {}
    direction_list = models.Direction.objects.all()
    level_list = models.Level.objects.all()
    if dr_id == "0":#未选择方向

        category_list = models.Category.objects.all()
        if cg_id == "0":#未选择分类
            pass
        else: #未选择方向，选择了分类
            condition["category_id"] =cg_id
    else:#选择方向
        category_list = models.Category.objects.filter(direction=dr_id)
        temp=category_list.values_list("id")
        #print(v)
        cg_id_list = list(zip(*temp))[0]
        #print(cg_id_list)
        if cg_id == "0":#选择了方向没有选择分类
            condition["category_id__in"]=cg_id_list
        else: #选择了方向也选择了分类
            if int(cg_id) in cg_id_list:
                condition["category_id"]=cg_id
            else:#请求的分类不在所有的分类中
                condition["category_id__in"] = cg_id_list
                kwargs["category_id"] = "0"
    if lv_id == "0":
        pass
    else:
        condition["level_id"]=lv_id
    result = models.Video.objects.filter(**condition)
    print(result)


    return render(request,"video/video2.html",{"direction_list":direction_list,
                                               "level_list":level_list,
                                               "category_list":category_list,
                                               "arg_list":kwargs})
