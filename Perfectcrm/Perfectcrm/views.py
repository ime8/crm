#-*-coding:utf-8 -*-
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render,redirect

def acc_login(request):
    """登陆页面"""
    error={}
    print("request.POST:",request.POST)
    if request.method == "POST":
        _email = request.POST.get("email")
        print("request.POST.get('email')",_email)
        _password = request.POST.get("password")
        print("request.POST.get('password')",_password)

        user = authenticate(email=_email,password=_password)
        print("user",user)
        if user:
            login(request, user)
            next_url = request.GET.get("next","/")
            print("next_url:",next_url)

            return redirect(next_url)
        else:
            error["error"]="email or password wrong"
    return render(request,"login.html",{"error":error})

def acc_logout(request):
    """退出页面"""
    logout(request)
    return redirect("/account/login/")

def index(request):

    return render(request,"index.html")