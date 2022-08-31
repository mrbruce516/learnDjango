# 部门管理视图

from django.shortcuts import render, redirect
from web import models
from web.utils.pagination import Pagination
from web.utils.search import Search
from web.utils.form import DepartModelForm


# Create your views here.

def depart_list(request):
    """ 部门管理中心 """

    query_title = Search(request, field_rule="title__contains")

    # 去数据库中获取所有部门信息
    depart = models.Department.objects.filter(**query_title.data_dict)

    page_obj = Pagination(request, queryset=depart)

    context = {
        'search': query_title.search,
        'depart': page_obj.page_queryset,
        'placeholder': "查找部门",
        'page_number': page_obj.html()
    }

    return render(request, 'depart_list.html', context)


def depart_add(request):

    if request.method == 'GET':
        context = {
            'title': "新增部门",
            'form': DepartModelForm()
        }
        return render(request, 'layout_add.html', context)

    form = DepartModelForm(data=request.POST)
    context = {
        'title': "新增部门",
        'form': form
    }
    if form.is_valid():
        form.save()
        # 重定向回主页面
        return redirect("/depart/list/")
    return render(request, 'layout_add.html', context)


def depart_del(request):
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list")


def depart_edit(request, nid):
    if request.method == 'GET':
        depart = models.Department.objects.filter(id=nid)
        return render(request, "depart_edit.html", {'depart': depart})

    # 获取数据并更新
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")
