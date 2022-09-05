import random
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web import models
from web.utils.form import OrderModelForm
from web.utils.pagination import Pagination


def order_list(request):
    queryset = models.Order.objects.all()
    page_obj = Pagination(request, queryset)

    form = OrderModelForm()
    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_number': page_obj.html()
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """ 新建订单 Ajax请求 """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.user_id = request.session["login_info"]["id"]
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def order_del(request):
    uid = request.GET.get("uid")
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


def order_detail(request):
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})
    result = {
        'status': True,
        'data': row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    uid = request.GET.get('uid')
    row_obj = models.Order.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({"status": False, "tips": "数据不存在"})
    form = OrderModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})
