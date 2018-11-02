"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from blog.views import home, api, admin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", home.index),
    path("index.html", home.index),
    path("article/<int:aid>.html", home.read_article),
    path("api/index", api.index),
    path("admin/login.html", admin.login_page),
    path("admin/index.html", admin.index_page),
    path("admin/articles.html", admin.articles_page),
    path("admin/write.html", admin.write_page),
    path("admin/delete_article.html", admin.delete_article)

]
