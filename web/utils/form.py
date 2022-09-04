from django import forms
from django.core.validators import RegexValidator
from django.core.validators import ValidationError
from web import models
from web.utils.encrpty import md5
from web.utils.bsmodelform import BootStrapModelForm


class DepartModelForm(BootStrapModelForm):
    """部门表单"""
    title = forms.CharField(min_length=3, label='部门名称')

    class Meta:
        model = models.Department
        fields = ["title"]


class UserModelForm(BootStrapModelForm):
    """用户表单"""
    # 这里定义规则与插件
    account = forms.CharField(label="用户名")
    name = forms.CharField(min_length=2, label='姓名')
    pwd = forms.CharField(min_length=6, label='密码', widget=forms.PasswordInput)
    confirm_pwd = forms.CharField(min_length=6, label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = models.UserInfo
        fields = ["account", "name", "gender", "pwd", "confirm_pwd", "depart", "create_time", "admin"]

    def clean_account(self):
        account = self.cleaned_data["account"]

        exist = models.UserInfo.objects.filter(account=account).exists()
        if exist:
            raise ValidationError("此用户名已存在")
        return account

    def clean_pwd(self):
        pwd = self.cleaned_data.get("pwd")
        return md5(pwd)

    def clean_confirm_pwd(self):
        pwd = self.cleaned_data.get("pwd")
        confirm = md5(self.cleaned_data.get("confirm_pwd"))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm


class UserEditModelForm(BootStrapModelForm):
    """编辑用户表单"""
    # 这里定义规则与插件
    account = forms.CharField(label="用户名")
    name = forms.CharField(min_length=2, label='姓名')
    pwd = forms.CharField(min_length=6, label='密码', widget=forms.PasswordInput)
    confirm_pwd = forms.CharField(min_length=6, label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = models.UserInfo
        fields = ["account", "name", "gender", "pwd", "confirm_pwd", "depart", "create_time", "admin"]

    def clean_account(self):
        account = self.cleaned_data["account"]
        user_id = self.instance.pk

        exist = models.UserInfo.objects.filter(account=account).exclude(id=user_id).exists()
        if exist:
            raise ValidationError("此用户名已存在")
        return account

    def clean_pwd(self):
        pwd = self.cleaned_data.get("pwd")
        return md5(pwd)

    def clean_confirm_pwd(self):
        pwd = self.cleaned_data.get("pwd")
        confirm = md5(self.cleaned_data.get("confirm_pwd"))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm


class PnumModelForm(BootStrapModelForm):
    """靓号表单"""
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


class PnumEditModelForm(BootStrapModelForm):
    """编辑靓号表单"""
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


"""
登陆校验功能(form版本)
    class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput
    )
"""


class LoginForm(BootStrapModelForm):
    pwd = forms.CharField(
        label="密码",
        widget=forms.PasswordInput
    )

    verify_code = forms.CharField(
        label="验证码",
    )

    class Meta:
        model = models.UserInfo
        fields = ["account", "pwd"]

    def clean_pwd(self):
        pwd = self.cleaned_data.get("pwd")
        return md5(pwd)


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid"]

