from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    """ 登陆鉴权中间件 """

    def process_request(self, request):
        # 排除不需要登陆的页面
        if request.path_info == "/login/":
            return

        login_info = request.session.get("login_info")
        if login_info:
            return  # 返回空，转发到下一个中间件或者直接加载视图函数
        return redirect('/login/')
