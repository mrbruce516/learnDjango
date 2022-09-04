from django.db import models
import uuid
from datetime import datetime


# Create your models here.

class Department(models.Model):
    """ 部门表 """
    id = models.UUIDField(verbose_name="id", primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(verbose_name="部门名称", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    id = models.UUIDField(verbose_name="id", primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    account = models.CharField(verbose_name="用户名", max_length=16)
    name = models.CharField(verbose_name="姓名", max_length=16)
    gender_choice = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)
    pwd = models.CharField(verbose_name="密码", max_length=64)
    balance = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", default=datetime.now)
    # 级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    admin_choice = (
        (0, "否"),
        (1, "是")
    )
    admin = models.PositiveSmallIntegerField(verbose_name="管理员", choices=admin_choice)

    def __str__(self):
        return self.name


class PrettyNum(models.Model):
    """ 商品：靓号表 """
    id = models.UUIDField(verbose_name="id", primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    mobile = models.CharField(verbose_name="号码", max_length=11)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)
    level_choice = (
        (1, "银"),
        (2, "金"),
        (3, "铂金"),
        (4, "钻石"),
    )
    level = models.PositiveSmallIntegerField(verbose_name="级别", choices=level_choice)
    status_choice = (
        (0, "未启用"),
        (1, "启用"),
    )
    status = models.PositiveSmallIntegerField(verbose_name="状态", choices=status_choice, default=0)


class Task(models.Model):
    """ 任务列表 """
    id = models.UUIDField(verbose_name="id", primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    level_choice = {
        (1, "普通"),
        (2, "重要"),
        (3, "临时")
    }
    level = models.PositiveSmallIntegerField(verbose_name="级别", choices=level_choice, default=1)
    title = models.CharField(verbose_name="标题", max_length=12)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="UserInfo", on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单 """
    id = models.UUIDField(verbose_name="id", primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    oid = models.CharField(verbose_name="订单号", max_length=32)
    title = models.CharField(verbose_name="名称", max_length=16)
    price = models.PositiveIntegerField(verbose_name="价格")
    status_choice = (
        (1, "已支付"),
        (2, "未支付")
    )
    status = models.PositiveSmallIntegerField(verbose_name="状态", choices=status_choice, default=2)
    user = models.ForeignKey(verbose_name="用户", to=UserInfo, on_delete=models.CASCADE)
