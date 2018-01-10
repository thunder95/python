# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from tagging.models import Tag
from tagging.fields import TagField
from tagging.registry import register

STATUS = {
        0: u'草稿',
        1: u'发布',
        2: u'删除',
}

EDITOR = [
    u'文本类型',
    u'程序类型',
]


# 复写TagField的sava方法，让它不做任何事
class TagField_Mine(TagField):
    def _save(self, **kwargs):
        pass


# class Editor(models.Model):
#     name = models.CharField(max_length=20, primary_key=True)
#     avaliable = models.BooleanField(default=True)
#
#     def __str__(self):
#        return self.name


class User(AbstractUser):
    name = models.CharField(max_length=12)
    # editor_choice = models.ForeignKey(Editor, null=True, blank=True, default="tinyMCE")
    editor_choice = models.CharField(max_length=20, default='tinyMCE')
    avatar_path = models.ImageField(upload_to="/avatar", default="/static/image/avatar_default.jpg")

    def __str__(self):
        return self.name


class Catalogue(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间
    modify_time = models.DateTimeField(auto_now_add=True)  # 每次保存自动更新时间
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    catalogue = models.ForeignKey(Catalogue)
    tag = TagField_Mine()
    view_count = models.IntegerField(editable=False, default=0)
    status = models.SmallIntegerField(default=0, choices=STATUS.items())  # 0为草稿，1为发布，2为删除
    # editor_choice = models.ForeignKey(Editor)
    editor_choice = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def update_tags(self, tag_name):
        # 把list转为string
        tag_str = "".join(tag_name)
        Tag.objects.update_tags(self, tag_str)

    def remove_tags(self):
        Tag.objects.update_tags(self, None)

    class Meta:
        ordering = ['-modify_time']


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    publish_Time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    content = models.TextField()
    root_id = models.IntegerField(default=0)  # 评论的最上层评论，若该评论处于最上层，则为0，
    parent_id = models.IntegerField(default=0)  # 评论的父评论，若无父评论，则为0

    def __str__(self):
        return self.content


class Carousel(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to="/carousel")
    post = models.ForeignKey(Post)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']


# 知识库模型
class Repository(models.Model):
    title = models.CharField(max_length=100)
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间
    author = models.CharField(max_length=20)
    content = models.TextField()
    tag = models.ManyToManyField(Tag, blank=True, default="")  # 外键tag可为空，外键被删除时该值设定为默认值“”
    view_count = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_time']

# 文档类型模型
class Docutype(models.Model):
    name = models.CharField(max_length=100)
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间, 后续不会更新
    modify_time = models.DateTimeField(auto_now=True)  # 每次保存自动更新时间, 后续会更新
    author = models.ForeignKey(settings.AUTH_USER_MODEL) # 保存当前用户的ID
    is_deleted = models.SmallIntegerField(default=0)  # 0为正常，1为已删除

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-modify_time']

# 产品名称模型
class Product(models.Model):
    name = models.CharField(max_length=100)
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间, 后续不会更新
    modify_time = models.DateTimeField(auto_now=True)  # 每次保存自动更新时间, 后续会更新
    author = models.ForeignKey(settings.AUTH_USER_MODEL) # 保存当前用户的ID
    description = models.CharField(max_length=255, default='') #简要描述
    docutype = models.ForeignKey(Docutype) #文档类型
    is_deleted = models.SmallIntegerField(default=0)  # 0为正常，1为已删除
    menu_json =  models.TextField(default='') #目录json数据

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-modify_time']

# 文档内容模型
class Content(models.Model):
    product = models.ForeignKey(Product) #文档ID
    menu_id = models.IntegerField(default=1)  # 目录id
    content = models.TextField(default='') #内容
    content_type = models.SmallIntegerField(default=0)  # 0为editor编辑器, 1为markdown编辑器
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间, 后续不会更新
    modify_time = models.DateTimeField(auto_now=True)  # 每次保存自动更新时间, 后续会更新

    def __str__(self):
        return str(self.menu_id)

    class Meta:
        ordering = ['-modify_time']

register(Product)