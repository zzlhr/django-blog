import re

from django.http import HttpResponse
from django.template.loader import get_template

from blog.views import admin


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        response = get_response(request)

        # 验证是否登录
        if re.search('/admin/(.*?)', request.path) and request.path != "/admin/login.html" and \
                admin.auth_token(request.get_signed_cookie("token", '')) == False:
            template = get_template('admin/login.html')
            context = {
                'website': admin.get_website_config(),
                'error_msg': '请先登录！'
            }
            return HttpResponse(template.render(context, request))

        return response

    return middleware
