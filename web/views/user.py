# 用户管理视图

from django.shortcuts import render, redirect
from web import models
from web.utils.pagination import Pagination
from web.utils.form import UserModelForm


# Create your views here.

def user_list(request):
    queryset = models.UserInfo.objects.all()

    page_obj = Pagination(request, queryset)

    context = {
        'queryset': page_obj.page_queryset,
        'page_number': page_obj.html()
    }

    return render(request, "user_list.html", context)


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, "user_add.html", {'form': form})

    # 校验用户提交的信息是否合法
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，则写入数据库
        # print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, "user_add.html", {'form': form})


def user_del(request):
    nid = request.GET.get("nid")
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def user_edit(request, nid):
    row_obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        # 根据id获取该用户所有信息
        # 把该用户信息带入编辑框
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {'form': form})

    # 校验用户提交的信息是否合法
    form = UserModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, "user_edit.html", {'form': form})
