import os
from django.shortcuts import render
from django.http import HttpResponse
from web import models
from web.utils.form import UploadForm, UploadModelForm


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


def upload_form(request):
    title = "Form上传"
    if request.method == 'GET':
        form = UploadForm()
        context = {
            'title': title,
            'form': form
        }
        return render(request, 'upload_form.html', context)

    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 1. 读取文件名，写入文件夹并获取写入路径
        avatar_obj = form.cleaned_data.get("avatar")
        media_path = os.path.join("media", "avatar", avatar_obj.name)
        f = open(media_path, mode='wb')
        for chunk in avatar_obj.chunks():
            f.write(chunk)
        f.close()

        # 2. 将图片路径写入数据库
        models.Avatar.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            avatar=media_path
        )
        return HttpResponse("添加成功")

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'upload_form.html', context)


def upload_modelform(request):
    title = "ModelForm上传"
    if request.method == 'GET':
        form = UploadModelForm()
        context = {
            'title': title,
            'form': form
        }
        return render(request, 'upload_modelform.html', context)
    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("上传成功")
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'upload_modelform.html', context)

