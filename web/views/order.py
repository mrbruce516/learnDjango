import random
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web.utils.form import OrderModelForm


def order_list(request):
    form = OrderModelForm()
    context = {
        'form': form
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """ 新建订单 Ajax请求 """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
