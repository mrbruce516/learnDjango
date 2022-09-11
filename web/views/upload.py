from django.shortcuts import render
from django.http import HttpResponse


def upload_list(request):
    if request.method == 'GET':
        return render(request, 'upload_list.html')
    file_obj = request.FILES.get("file")
    # 以二进制写入模式打开文件对象
    file = open(file_obj.name, mode='wb')
    # 块模式写入到服务端中
    for chunk in file_obj.chunks():
        file.write(chunk)
    file.close()
    return HttpResponse("文件上传成功")
