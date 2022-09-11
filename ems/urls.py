"""ems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web.views import depart, user, pnum, task, order, chart, upload

urlpatterns = [
    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/batch-add/', depart.depart_batch_add),
    path('depart/del/', depart.depart_del),
    path('depart/<uuid:nid>/edit/', depart.depart_edit),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/del/', user.user_del),
    path('user/<uuid:nid>/edit/', user.user_edit),
    path('login/', user.login),
    path('logout/', user.logout),
    path('login/verify/', user.login_verify),

    # 靓号管理
    path('pnum/list/', pnum.pnum_list),
    path('pnum/add/', pnum.pnum_add),
    path('pnum/<uuid:nid>/edit/', pnum.pnum_edit),
    path('pnum/del/', pnum.pnum_del),

    # 任务管理
    path('task/list/', task.task_list),
    path('task/add/', task.task_add),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/del/', order.order_del),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),

    # 上传文件
    path('upload/list/', upload.upload_list),
]
