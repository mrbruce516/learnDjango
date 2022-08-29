"""
自定义的分页组件,使用它需要下面几个步骤

在视图中的函数
def pnum_list(request):
    # 1. 筛选你需要查询的数据
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-price")

    # 2. 实例化Pagination类，传入查询参数
    page_obj = Pagination(request, queryset)

    # 3. 使用分页功能模块
    context = {
        'search_mobile': search_mobile,
        'queryset': page_obj.page_queryset,  # 列表数据
        'page_number': page_obj.html()  # 分页功能
    }

    # 4. 返回页面
    return render(request, 'pnum_list.html', context)

在HTML中
<!-- 显示分页数据 /-->
{% for obj in queryset %}
    {{ obj.xx }}
{% endfor %}

<!-- 生成分页 /-->
<ul class="pagination" style="float: left;">
    {{ page_number }}
</ul>

"""
from django.utils.safestring import mark_safe
import copy


class Pagination(object):

    # web请求，查询语句，分页大小，获取页码，显示前后5页
    def __init__(self, request, queryset, page_size=12, page_param="page", plus=5):

        #  拷贝查询参数
        query_dict = copy.deepcopy(request.GET)
        # 使GET请求的数组为可编辑状态
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_parm = page_param

        # 获取当前页码
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        # 提供从[第x条到第x条]的数据
        self.page_queryset = queryset[self.start:self.end]

        # 数据总条数
        total_count = queryset.count()
        # 总页码数量，divmod商，余数(总条数，每页显示多少条)
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

        self.plus = plus

    def html(self):
        # 页码
        page_list = []

        # 当数据库条数比较少时，就显示固定的页码范围，不筛减范围
        if self.total_page_count <= 2 * self.plus + 1:
            front_page = 1
            behind_page = self.total_page_count
        else:
            # 数据库的数据比较多(处理最小值)
            if self.page <= self.plus:
                front_page = 1
                behind_page = 2 * self.plus + 1
            # 处理最大值
            elif self.page + self.plus >= self.total_page_count:
                front_page = self.total_page_count - 2 * self.plus
                behind_page = self.total_page_count
            # 中间部分
            else:
                front_page = self.page - self.plus
                behind_page = self.page + self.plus

        # 首页
        self.query_dict.setlist(self.page_parm, [1])
        first = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        if self.page == self.page == 1 or self.total_page_count == 0:
            first = '<li class="disabled"><span>首页</span></li>'
        page_list.append(first)

        # 上一页
        self.query_dict.setlist(self.page_parm, [self.page - 1])
        perv = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        if self.page == 1:
            perv = '<li class="disabled"><span>上一页</span></li>'
        page_list.append(perv)

        # 中间页，因为range函数 前取后不取，所以+1
        for i in range(front_page, behind_page + 1):
            self.query_dict.setlist(self.page_parm, [i])
            if i == self.page:
                # 高亮显示当前页号
                num = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                num = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_list.append(num)

        # 下一页
        self.query_dict.setlist(self.page_parm, [self.page + 1])
        tsugi = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        if self.page == self.total_page_count or self.total_page_count == 0:
            tsugi = '<li class="disabled"><span>下一页</span></li>'
        page_list.append(tsugi)

        # 尾页
        self.query_dict.setlist(self.page_parm, [self.total_page_count])
        if self.total_page_count == 0:
            self.query_dict.setlist(self.page_parm, [1])
            tail = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        else:
            tail = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        if self.page == self.total_page_count or self.total_page_count == 0:
            tail = '<li class="disabled"><span>尾页</span></li>'
        page_list.append(tail)

        # 输入跳转框
        jump_num = """
            <li>
                <form method="get" style="float: left;margin-left: -1px;">
                    <input type="text" name="page" class="form-control" placeholder="页码"
                           style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0px;">
                    <button style="border-radius: 0px" class="btn btn-default" type="submit">跳转</button>
                </form>
            </li>
        """
        page_list.append(jump_num)

        # 生成页码
        page_number = mark_safe("".join(page_list))
        return page_number
