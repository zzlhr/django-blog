from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
import markdown
from blog.models import Website, User, Article, ArticleInfo
from blog.util import md5


def get_website_config():
    website = list(Website.objects.all())[0]
    return website


def login_page(request):
    if request.method == "GET":
        template = get_template('admin/login.html')
        context = {'website': get_website_config()}
        return HttpResponse(template.render(context, request))
    if request.method == "POST":
        login_name = request.POST.get("login_name")
        password = request.POST.get("password")
        user = User.objects.filter(login_name=login_name).first()
        password = md5.encrypt_user_password(password)

        if user.password != password:
            template = get_template('admin/login.html')
            context = {
                'website': get_website_config(),
                'error_msg': '用户名或密码错误！'
            }
            return HttpResponse(template.render(context, request))

        return HttpResponseRedirect("index.html")


def index_page(request):
    if request.method == "GET":
        template = get_template("admin/index.html")
        context = {
            'website': get_website_config(),
        }
        return HttpResponse(template.render(context, request))


def articles_page(request):
    if request.method == "GET":

        article_list = list(Article.objects.all().order_by('-create_time')[:10])

        article_info_list = list(ArticleInfo.objects.filter(aid__in=(map(lambda a: a.aid, article_list))).all())

        for _article in article_list:
            for article_info in article_info_list:
                if article_info.aid == _article.aid:
                    _article.article_info = article_info

        template = get_template("admin/articles.html")

        context = {
            'website': get_website_config(),
            'articles': article_list
        }
        return HttpResponse(template.render(context, request))
