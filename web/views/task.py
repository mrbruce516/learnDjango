import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from web.utils.form import TaskModelForm


def task_list(request):
    form = TaskModelForm()
    context = {
        'form': form
    }
    return render(request, 'task_list.html', context)


@csrf_exempt
def task_add(request):
    # print(request.POST)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {
        'status': False,
        'error': form.errors
    }
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
