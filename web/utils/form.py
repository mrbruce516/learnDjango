from django import forms
from django.core.validators import RegexValidator
from django.core.validators import ValidationError
from web.utils.bsmodelform import BootStrapModelForm
from web import models


# 部门表单
class DepartModelForm(BootStrapModelForm):
    title = forms.CharField(min_length=3, label='部门名称')

    class Meta:
        model = models.Department
        fields = ["title"]


# 用户表单, user_add, user_edit 使用
class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=2, label='姓名')
    pwd = forms.CharField(min_length=6, label='密码')

    class Meta:
        model = models.UserInfo
        fields = ["account", "name", "gender", "pwd", "depart", "create_time", "admin"]


# 添加靓号表单，pnum_add 使用
class PnumModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        label='号码',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        # __all__表示所有字段, exclude表示排除某个字段
        fields = "__all__"

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("该手机号已存在")
        return txt_mobile


# 编辑靓号表单，pnum_edit 使用
class PnumEditModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        label='号码',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        # __all__表示所有字段, exclude表示排除某个字段
        fields = "__all__"

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # pk 代表主键
        mobile_id = self.instance.pk

        # 排除自己，不能与其他手机号重复
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exclude(id=mobile_id).exists()
        if exists:
            raise ValidationError("该手机号已存在")
        return txt_mobile
