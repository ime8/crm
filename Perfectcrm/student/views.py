from django.shortcuts import render,HttpResponse
from PerfectCRM.Perfectcrm.crm import models
from PerfectCRM.Perfectcrm.Perfectcrm import settings
import os,json

# Create your views here.
def stu_my_class(request):
    #enrollment_set通过stu_account里逆向找enrollment_set.all()找到表Enrollment所有数据
    print("request.user.stu_account.enrollment_set.all",request.user.stu_account)
    return render(request,"student/index.html")

def mycourse(request,enroll_id):
    """我的课程页面"""
    #找到报名表对象
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    return render(request,"student/mycourse.html",{"enroll_obj":enroll_obj})

def my_homework(request,studyscore_id):
    """我的作业"""
    studyscore_obj = models.StudyRecord.objects.get(id=studyscore_id)
    if request.method == "POST":
        #print("request.FILES:",request.FILES)
        if request.is_ajax():
            homework_path = "{base_dir}/{class_id}/{course_recored_id}/{studycords_id}".\
                format(base_dir=settings.HOMEWORK_DATA,class_id=studyscore_obj.student.enrolled_class_id,
                       course_recored_id=studyscore_obj.course_record_id,studycords_id=studyscore_obj.id)
            if not os.path.isdir(homework_path):
                os.makedirs(homework_path,exist_ok=True)
            for k,file_obj in request.FILES.items():
                with open("%s/%s"%(homework_path,file_obj.name),"wb") as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)
            return HttpResponse(json.dumps({"status":0,"msg":"file upload success"}))
    return render(request,"student/my_homework.html",{"studyscore_obj":studyscore_obj})