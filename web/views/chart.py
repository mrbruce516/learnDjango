from django.shortcuts import render
from django.http import JsonResponse
from web import models


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    legend = ['黑暗之魂3', '老头环']
    series = [
        {
            'name': "黑暗之魂3",
            'type': "bar",
            "data": [16, 23, 34]
        },
        {
            'name': "老头环",
            'type': "bar",
            'data': [12, 32, 43]
        }
    ]
    x_axis = ['1月', '2月', '3月']
    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series': series,
            'xAxis': x_axis
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    db_query_list = [
        {"value": 1048, "name": '老头环'},
        {"value": 1735, "name": '原神3.0'},
        {"value": 580, "name": 'CS:GO'},
        {"value": 484, "name": 'LoL'},
        {"value": 300, "name": '黑暗之魂3'}
    ]
    result = {
        "status": True,
        "data": db_query_list
    }
    return JsonResponse(result)


def chart_line(request):
    data = [10, 23, 54, 23, 6, 34, 12]
    result = {
        'status': True,
        'data': data
    }
    return JsonResponse(result)
