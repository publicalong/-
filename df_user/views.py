# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect

from hashlib import sha1
from models import *

def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    # 接受对象
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd1= post.get('cpwd')
    uemail = post.get('email')
    #判断两次的密码是否相等
    if upwd!=upwd1:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd2 = s1.hexdigest()
    #存储到数据库
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd2
    user.uemail = uemail
    user.save()
    # 注册成功，转到登陆页面
    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context={'title':'用户登陆','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    # 默认jizhu为0,当没有点击记住密码时，不会提交过来，使用默认的数据0,当提交过来时，会使用提交的值1
    jizhu = post.get('jizhu',0)
    # 查询数据库中的对应的uname对象，使用filter 查到返回对应的列表，查不到返回[]
    user = UserInfo.objects.filter(uname=uname)
    # 判断是否查到对象
    if len(user)==1:
        s1 =sha1()
        s1.update(upwd)
        if s1.hexdigest()==user[0].upwd:
            # 创建一个对象（由于要使用cookie），用于返回到用户中心
            red = HttpResponseRedirect('user/info')
            # 记住用户名的操作,使用cookie存储
            if jizhu!=0:
                red.set_cookie('uname', uname)
            else:
                # 不存储密码时，设置过期时间为立即过期
                red.set_cookie('uname', '', max_age=-1)
                request.session['user_id']=user[0].id
                request.session['user_name']=uname

            return red
        else:
            context = {'title':'用户登陆', 'error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html', context)
    else:
        context = {'title': '用户登陆', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, "df_user/login.html", context)
