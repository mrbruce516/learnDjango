from django.shortcuts import render, redirect
from web import models
from django import forms
from django.core.validators import RegexValidator
from django.core.validators import ValidationError
from web.utils.pagination import Pagination


# Create your views here.

def depart_list(request):
    """ 部门管理中心 """

    # 去数据库中获取所有部门信息
    depart = models.Department.objects.all()

    page_obj = Pagination(request, queryset=depart)

    context = {
        'depart': page_obj.page_queryset,
        'page_number': page_obj.html()
    }

    return render(request, 'depart_list.html', context)


def depart_add(request):
    if request.method == 'GET':
        return render(request, 'depart_add.html')

    # 获取用户提交的数据
    title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回主页面
    return redirect("/depart/list/")


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


def user_list(request):
    queryset = models.UserInfo.objects.all()

    page_obj = Pagination(request, queryset)

    context = {
        'queryset': page_obj.page_queryset,
        'page_number': page_obj.html()
    }

    return render(request, "user_list.html", context)


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=2, label='姓名')
    pwd = forms.CharField(min_length=6, label='密码')

    class Meta:
        model = models.UserInfo
        fields = ["name", "gender", "pwd", "depart", "create_time"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control"}


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


def pnum_list(request):
    # 创建测试数据
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="18173465432", level=1)

    # 搜索
    data_dict = {}
    search_mobile = request.GET.get('q', '')
    if search_mobile:
        data_dict["mobile__contains"] = search_mobile

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-price")

    # 实例化Pagination类，传入查询参数
    page_obj = Pagination(request, queryset)

    context = {
        'search_mobile': search_mobile,
        'queryset': page_obj.page_queryset,  # 列表数据
        'page_number': page_obj.html()  # 分页功能
    }

    return render(request, 'pnum_list.html', context)


class PnumModelForm(forms.ModelForm):
    mobile = forms.CharField(
        label='号码',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        # __all__表示所有字段, exclude表示排除某个字段
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control"}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("该手机号已存在")
        return txt_mobile


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


class PnumEditModelForm(forms.ModelForm):
    mobile = forms.CharField(
        label='号码',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        # __all__表示所有字段, exclude表示排除某个字段
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control"}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # pk 代表主键
        mobile_id = self.instance.pk

        # 排除自己，不能与其他手机号重复
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exclude(id=mobile_id).exists()
        if exists:
            raise ValidationError("该手机号已存在")
        return txt_mobile


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
