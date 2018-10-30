# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Article(models.Model):
    aid = models.AutoField(primary_key=True)
    article_title = models.CharField(max_length=300)
    article_describe = models.CharField(max_length=255)
    article_content_html = models.TextField()
    article_content_md = models.TextField(blank=True, null=True)
    article_author = models.PositiveIntegerField()
    article_status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article'


class ArticleComment(models.Model):
    article_id = models.IntegerField()
    user_id = models.IntegerField()
    comment_content = models.CharField(max_length=1000, blank=True, null=True)
    comment_status = models.IntegerField(blank=True, null=True)
    comment_ip = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article_comment'


class ArticleInfo(models.Model):
    aid = models.PositiveIntegerField(primary_key=True)
    article_click = models.IntegerField()
    article_comment = models.IntegerField()
    article_zan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'article_info'


class ArticlePlace(models.Model):
    place_tag = models.CharField(max_length=20)
    place_value = models.CharField(max_length=100)
    place_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article_place'


class ArticleStatistics(models.Model):
    statistics_name = models.CharField(max_length=50)
    statistics_type = models.IntegerField()
    statistics_value = models.CharField(max_length=20)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article_statistics'


class ArticleTag(models.Model):
    atid = models.AutoField(primary_key=True)
    aid = models.IntegerField()
    tag_content = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'article_tag'


class AuthCode(models.Model):
    ac_id = models.CharField(primary_key=True, max_length=32)
    ip = models.CharField(max_length=45)
    value = models.CharField(max_length=20)
    create_time = models.DateTimeField()
    used = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_code'


class FriendLink(models.Model):
    value = models.CharField(max_length=20)
    url = models.CharField(max_length=255)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'friend_link'


class Log(models.Model):
    user_name = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    user_ip = models.CharField(max_length=20, blank=True, null=True)
    operation = models.CharField(max_length=255)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log'


class Tag(models.Model):
    tag_content = models.CharField(max_length=20)
    tag_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tag'


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    login_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128, blank=True, null=True)
    token = models.CharField(max_length=128, blank=True, null=True)
    header_url = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    last_login_ip = models.CharField(max_length=20, blank=True, null=True)
    last_login_address = models.CharField(max_length=30, blank=True, null=True)
    status = models.IntegerField()
    admin = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Website(models.Model):
    host = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    keywords = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    master_name = models.CharField(max_length=50, blank=True, null=True)
    master_email = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website'

