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
