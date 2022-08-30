# 靓号管理视图

from django.shortcuts import render, redirect
from web import models
from web.utils.pagination import Pagination
from web.utils.form import PnumModelForm, PnumEditModelForm
from web.utils.search import Search


# Create your views here.

def pnum_list(request):
    # 创建测试数据
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="18173465432", level=1)

    data_dict = Search(request, field_rule="mobile__contains")

    queryset = models.PrettyNum.objects.filter(**data_dict.data_dict).order_by("-price")

    # 实例化Pagination类，传入查询参数
    page_obj = Pagination(request, queryset)

    context = {
        'search': data_dict.search,
        'placeholder': "查找手机号",
        'queryset': page_obj.page_queryset,  # 列表数据
        'page_number': page_obj.html()  # 分页功能
    }

    return render(request, 'pnum_list.html', context)


def pnum_add(request):
    if request.method == 'GET':
        form = PnumModelForm()
        return render(request, 'pnum_add.html', {'form': form})

    # 校验用户提交的信息是否合法
    form = PnumModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，则写入数据库
        # print(form.cleaned_data)
        form.save()
        return redirect('/pnum/list/')
    return render(request, "pnum_add.html", {'form': form})


def pnum_edit(request, nid):
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        # 根据id获取该用户所有信息
        # 把该用户信息带入编辑框
        form = PnumEditModelForm(instance=row_obj)
        return render(request, 'pnum_edit.html', {'form': form})

    # 校验用户提交的信息是否合法
    form = PnumEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/pnum/list/')
    return render(request, "pnum_edit.html", {'form': form})


def pnum_del(request):
    nid = request.GET.get("nid")
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pnum/list")
