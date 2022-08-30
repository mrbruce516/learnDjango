"""
搜索功能，使用它需要如下步骤：

1. 实例化对象
query_xxx = Search(request, field_rule="mobile__contains")

2. 查询带入字典中的值
queryset = models.PrettyNum.objects.filter(**data_dict.data_dict)

3. 页面传入查询对象,用于查询后保留查询内容
return render(request, 'pnum_list.html', {'search': data_dict.search})
"""


class Search(object):

    # web请求，查询规则，参数名称
    def __init__(self, request, field_rule, query_parm='q'):
        self.data_dict = {}
        self.search = request.GET.get(query_parm, '')
        if self.search:
            self.data_dict[field_rule] = self.search
