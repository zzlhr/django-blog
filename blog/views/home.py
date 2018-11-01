from django.http import HttpResponse
from django.template.loader import get_template
import markdown

from blog.models import Article, ArticleInfo, FriendLink


def index(request):
    article_list = list(Article.objects.all().order_by('-create_time')[:10])

    article_info_list = list(ArticleInfo.objects.filter(aid__in=(map(lambda a: a.aid, article_list))).all())

    for _article in article_list:
        for article_info in article_info_list:
            if article_info.aid == _article.aid:
                _article.article_info = article_info

    template = get_template('index.html')
    context = {
        'article_list': article_list,
    }
    return HttpResponse(template.render(context, request))


def read_article(request, aid):
    _article = Article.objects.filter(aid=aid).first()

    if _article is None:
        return HttpResponse(status=404)

    print(_article)
    _article.article_info = ArticleInfo.objects.filter(aid=aid).first()

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
    }
    return HttpResponse(template.render(context, request))
