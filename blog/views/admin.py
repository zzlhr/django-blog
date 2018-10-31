from django.http import HttpResponse
from django.template.loader import get_template
import markdown
from blog.models import Website
from django.forms import Form
from django.forms import widgets  # 插件
from django.forms import fields  # 字段


def get_website_config():
    website = list(Website.objects.all())[0]
    return website


def login_page(request):
    template = get_template('admin/login.html')
    context = {'website': get_website_config()}
    return HttpResponse(template.render(context, request))


def login(Form):
    print(Form.POST.get("email"))
    print(Form.POST.get("password"))
    return HttpResponse("test")
