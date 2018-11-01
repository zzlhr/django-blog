from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.utils import timezone

from blog.models import Website, User, Article, ArticleInfo
from blog.util import md5
import uuid


# 认证token方法，返回true为通过，反之不通过
def auth_token(token):
    print("【认证token】token=" + token)
    if token == "":
        return False
    users = list(User.objects.filter(token=token).all())
    if len(users) == 0:
        return False

    return True


def token_get_user(token):
    return list(User.objects.filter(token=token).all())[0]


# 获取网站基础信息
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

        user.token = md5.encrypt(str(uuid.uuid1()))
        user.save()
        resp = HttpResponseRedirect("index.html")
        resp.set_signed_cookie("token", user.token)
        return resp


def index_page(request):
    if request.method == "GET":
        template = get_template("admin/index.html")
        context = {
            'website': get_website_config(),
        }
        return HttpResponse(template.render(context, request))


def articles_page(request):
    if request.method == "GET":
        limit = 10
        articles = Article.objects.all().order_by('-create_time')
        paginator = Paginator(articles, limit)  # 按每页10条分页
        page = request.GET.get('page', '1')  # 默认跳转到第一页
        result = paginator.page(page)

        # 查询article info
        aids = map(lambda a: a.aid, result)
        print(aids)
        article_info_list = list(ArticleInfo.objects.filter(aid__in=aids).all())

        for _article in result:
            for article_info in article_info_list:
                if article_info.aid == _article.aid:
                    _article.article_info = article_info

        template = get_template("admin/articles.html")

        context = {
            'website': get_website_config(),
            'articles': result
        }
        return HttpResponse(template.render(context, request))


def wrtie_page(request):
    if request.method == "GET":
        template = get_template("admin/write.html")

        context = {
            'website': get_website_config(),
        }
        return HttpResponse(template.render(context, request))

    if request.method == "POST":
        article_title = request.POST.get("article_title")
        article_describe = request.POST.get("article_describe")
        article_content_md = request.POST.get("article_content")
        user = token_get_user(request.get_signed_cookie("token"))
        article_status = 0
        print(user)
        article = Article(article_title=article_title, article_describe=article_describe,
                          article_content_md=article_content_md, article_author=user.uid,
                          article_status=article_status, create_time=timezone.now(),
                          update_time=timezone.now())
        article.save()
        template = get_template("admin/write_success.html")
        context = {
            'website': get_website_config(),
            'msg': {
                'title': '添加文章成功！',
                'info': '您下面可以返回列表进行查看，或者对本次添加文章进行修改',
                'links': [
                    {
                        'href': '/admin/articles.html',
                        'name': '返回列表'
                    },
                    {
                        'href': '/admin/edit_article.html?aid=' + str(article.aid),
                        'name': '编辑文章'
                    }
                ]
            }
        }
        return HttpResponse(template.render(context, request))
