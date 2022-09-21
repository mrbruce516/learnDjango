"""
自定义ModelForm类，并添加BootStrap样式

使用此类需要如下操作
class xxx(BootStrapModelForm):
    # 获取元数据
    class Meta:
        model = models.PrettyNum
        # fields = ["mobile", "price", "level", "status"]
        # __all__表示所有字段, exclude表示排除某个字段
        fields = "__all__"
"""
from django import forms


class BootStrap:
    exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段，给每个字段设置插件
        for name, field, in self.fields.items():
            if name in self.exclude_fields:
                continue
            # 字段中有属性的话，保留原来的属性，再添加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            # 如果字段中没有属性的话，直接创建字典写入BS属性
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass
