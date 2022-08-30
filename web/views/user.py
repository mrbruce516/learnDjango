# 用户管理视图

from django.shortcuts import render, redirect
from web import models
from web.utils.pagination import Pagination
from web.utils.form import UserModelForm, PnumModelForm, PnumEditModelForm


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

