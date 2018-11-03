from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.utils import timezone

from blog.models import Website, User, Article, ArticleInfo, ArticleTag
from blog.util import md5
import uuid


# 认证token方法，返回true为通过，反之不通过
def auth_token(token):
    print("【认证token】token=" + token)
    if token == "":
        return False
    users = list(User.objects.filter(token=token))
    if len(users) == 0:
        return False

    return True


def token_get_user(token):
    return list(User.objects.filter(token=token))[0]


# 获取网站基础信息
def get_website_config():
    website = list(Website.objects.all())[0]
    return website


# 登录
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


# 后台首页
def index_page(request):
    if request.method == "GET":
        template = get_template("admin/index.html")
        context = {
            'website': get_website_config(),
        }
        return HttpResponse(template.render(context, request))


# 文章列表
def articles_page(request):
    if request.method == "GET":
        limit = 10
        articles = Article.objects.filter(article_status=0).order_by('-create_time')
        paginator = Paginator(articles, limit)  # 按每页10条分页
        page = request.GET.get('page', '1')  # 默认跳转到第一页
        result = paginator.page(page)

        # 查询article info
        aids = map(lambda a: a.aid, result)
        print(aids)
        article_info_list = list(ArticleInfo.objects.filter(aid__in=aids))

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


# 写文章
def write_page(request):
    if request.method == "GET":
        aid = request.GET.get("aid", 0)
        article = None
        if aid != 0:
            # 编辑
            result = Article.objects.filter(aid=aid)
            article = result[0]
            _article_tag = list(ArticleTag.objects.filter(aid=aid))
            article_tag_val = ""
            for t in _article_tag:
                article_tag_val += t.tag_content + ","

            article.article_tag = article_tag_val[0:len(article_tag_val) - 1]

        template = get_template("admin/write.html")
        context = {
            'website': get_website_config(),
            'article': article
        }
        return HttpResponse(template.render(context, request))

    if request.method == "POST":

        article_title = request.POST.get("article_title")
        article_describe = request.POST.get("article_describe")
        article_content_md = request.POST.get("article_content")
        user = token_get_user(request.get_signed_cookie("token"))
        tags = request.POST.get("tag_content")
        article_status = 0
        article = Article(article_title=article_title, article_describe=article_describe,
                          article_content_md=article_content_md, article_author=user.uid,
                          article_status=article_status, create_time=timezone.now(),
                          update_time=timezone.now())
        if request.POST.get("aid") != "":
            # 编辑
            article.aid = request.POST.get("aid")

        article.save()

        if request.POST.get("aid") == "":
            # 添加需要初始化文章点击数评论数点赞数
            ArticleInfo(aid=article.aid, article_click=0, article_comment=0, article_zan=0).save()

        if request.POST.get("aid") != "":
            # 如果是编辑先删除之前的标签
            ArticleTag.objects.filter(aid=request.POST.get("aid")).delete()
        # 添加标签
        tag = tags.split(",")
        for t in tag:
            ArticleTag(tag_content=t, aid=article.aid).save()

        template = get_template("admin/result.html")
        context = {
            'website': get_website_config(),
            'msg': {
                'title': request.POST.get("aid") != "" if "编辑文章成功！" else "添加文章成功!",
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


def delete_article(request):
    if request.method == "GET":
        aid = request.GET.get("aid")
        result = Article.objects.filter(aid=aid, article_status=0)
        template = get_template("admin/result.html")

        if len(result) > 0:
            result.update(article_status=1)
            context = {
                'website': get_website_config(),
                'msg': {
                    'title': '删除文章成功！',
                    'info': '您下面可以返回列表进行查看。',
                    'links': [
                        {
                            'href': '/admin/articles.html',
                            'name': '返回列表'
                        }
                    ]
                }
            }
            return HttpResponse(template.render(context, request))
        else:
            context = {
                'website': get_website_config(),
                'msg': {
                    'title': '删除文章失败，改文章可能已被删除。',
                    'info': '您下面可以返回列表进行查看。',
                    'links': [
                        {
                            'href': '/admin/articles.html',
                            'name': '返回列表'
                        }
                    ]
                }
            }
            return HttpResponse(template.render(context, request))


def about_page(request):
    if request.method == "GET":
        template = get_template("admin/about.html")

        context = {
            'website': get_website_config(),
        }
        return HttpResponse(template.render(context, request))
    if request.method == "POST":
        about = request.POST.get("website_about")
        website = Website.objects.filter(id=1)[0]
        print(website)
        website.website_about = about
        website.save()
        template = get_template("admin/about.html")

        context = {
            'website': get_website_config(),
            'msg': '保存成功！'
        }
        return HttpResponse(template.render(context, request))