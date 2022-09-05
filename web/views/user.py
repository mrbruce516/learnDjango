# 用户管理视图

from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from web import models
from web.utils.search import Search
from web.utils.verify import check_code
from web.utils.pagination import Pagination
from web.utils.form import UserModelForm, UserEditModelForm, LoginForm


# Create your views here.

def user_list(request):
    query_account = Search(request, field_rule="account__contains")

    queryset = models.UserInfo.objects.filter(**query_account.data_dict)

    page_obj = Pagination(request, queryset)

    context = {
        'search': query_account.search,
        'placeholder': "查找用户名",
        'queryset': page_obj.page_queryset,
        'page_number': page_obj.html()
    }

    return render(request, "user_list.html", context)


def user_add(request):
    if request.method == 'GET':
        context = {
            'title': "新建用户",
            'form': UserModelForm(),
        }
        return render(request, "add.html", context)

    # 校验用户提交的信息是否合法
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，则写入数据库
        # print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    else:
        context = {
            'title': "新建用户",
            'form': form,
        }
        return render(request, "add.html", context)


def user_del(request):
    nid = request.GET.get("nid")
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def user_edit(request, nid):
    row_obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        # 根据id获取该用户所有信息
        # 把该用户信息带入编辑框
        context = {
            'title': "编辑用户",
            'form': UserEditModelForm(instance=row_obj)
        }
        return render(request, 'edit.html', context)
    # 校验用户提交的信息是否合法
    form = UserEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        context = {
            'title': "编辑用户",
            'form': form
        }
        return render(request, "edit.html", context)


def login(request):
    """登陆功能"""
    if request.method == "GET":
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context)
    form = LoginForm(data=request.POST)
    context = {
        'form': form
    }
    if form.is_valid():

        # 先认证验证码
        verify_code = form.cleaned_data.pop('verify_code')
        real_code = request.session.get('login_verify', "")
        if verify_code.upper() != real_code.upper():
            form.add_error("verify_code", "验证码输入错误")
            return render(request, 'login.html', context)

        login_data = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not login_data:
            form.add_error("pwd", "用户名或密码错误")
            return render(request, 'login.html', context)
        # 用户密码输入正确，写入用户浏览器cookie中，在写入服务端session中
        request.session["login_info"] = {
            'id': login_data.id.hex,
            'account': login_data.account,
            'name': login_data.name
        }
        # 7天免登陆
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/user/list/")
    return render(request, 'login.html', context)


def login_verify(request):
    """生成图片验证码"""
    img, code_str = check_code()

    # 写入验证码到session中
    request.session['login_verify'] = code_str
    # 设定超时时间（秒）
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())


def logout(request):
    """注销功能"""
    request.session.clear()
    return redirect('/login/')
