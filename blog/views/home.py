from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
import markdown

from blog.models import Article, ArticleInfo, FriendLink
from blog.views.admin import get_website_config


def index(request):
    limit = 10
    article_list = Article.objects.filter(article_status=0).order_by('-create_time')
    paginator = Paginator(article_list, limit)  # 按每页10条分页
    page = request.GET.get('page', '1')  # 默认跳转到第一页
    result = paginator.page(page)
    article_info_list = ArticleInfo.objects.filter(aid__in=(map(lambda a: a.aid, result)))

    for _article in result:
        for article_info in article_info_list:
            if article_info.aid == _article.aid:
                _article.article_info = article_info

    template = get_template('index.html')
    context = {
        'articles': result,
        'website': get_website_config(),
    }
    return HttpResponse(template.render(context, request))


def read_article(request, aid):
    _article = Article.objects.filter(aid=aid).first()

    if _article is None:
        return HttpResponse(status=404)

    article_info_result = ArticleInfo.objects.filter(aid=aid)

    # article_info_result[0].article_click = article_info_result[0].article_click + 1
    article_info_result.update(article_click=article_info_result[0].article_click + 1)

    _article.article_info = article_info_result[0]

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    _article.article_content_html = md.convert(_article.article_content_md)
    _article.toc = md.toc

    template = get_template('article.html')
    context = {
        'article': _article,
        'website': get_website_config(),
    }
    return HttpResponse(template.render(context, request))
