# -*- coding:utf-8 -*-
from __future__ import division

import datetime
import json
import os
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.views.generic import View, ListView, CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from zer0Blog.settings import MEDIA_ROOT, MEDIA_URL, image_type

from zer0Blog.settings import PERNUM
from blog.pagination import paginator_tool
from .models import Post, Catalogue, Carousel, User, EDITOR, Product, Docutype, Content
from thumbnail import ThumbnailTool
from PIL import Image


@csrf_exempt
def markdown_image_upload_handler(request):
    # 要返回的数据字典，组装好后，序列化为json格式
    if request.method == "POST":
        result = {}
        try:
            file_img = request.FILES['editormd-image-file']
            file_suffix = os.path.splitext(file_img.name)[len(os.path.splitext(file_img.name)) - 1]
            filename = uuid.uuid1().__str__() + file_suffix

            # 检查图片格式
            if file_suffix not in image_type:
                result['success'] = 0
                result['message'] = "上传失败，图片格式不正确"
            else:
                path = MEDIA_ROOT + "/post/"
                if not os.path.exists(path):
                    os.makedirs(path)

                # 图片宽大于825的时候，将其压缩到824px，刚好适合13吋pc的大小
                img = Image.open(file_img)
                width, height = img.size
                if width > 824:
                    img = ThumbnailTool.constrain_thumbnail(img, times=width/824.0)

                file_name = path + filename
                img.save(file_name)

                file_img_url = "http://" + request.META['HTTP_HOST'] + MEDIA_URL + "post/" + filename

                result['success'] = 1
                result['message'] = "上传成功"
                result['url'] = file_img_url

        except Exception, e:
            result['success'] = 0
            result['message'] = e
            print e

        return HttpResponse(json.dumps(result))


@csrf_exempt
def tinymce_image_upload_handler(request):
    if request.method == "POST":
        try:
            file_img = request.FILES['tinymce-image-file']
            file_suffix = os.path.splitext(file_img.name)[len(os.path.splitext(file_img.name)) - 1]
            # 检查图片格式
            if file_suffix not in image_type:
                return HttpResponse("请上传正确格式的图片文件")
            filename = uuid.uuid1().__str__() + file_suffix

            # 图片宽大于824的时候，将其压缩到824px，刚好适合13吋pc的大小
            img = Image.open(file_img)
            width, height = img.size
            if width > 824:
                img = ThumbnailTool.constrain_thumbnail(img, times=width/824.0)

            path = MEDIA_ROOT + "/post/"
            if not os.path.exists(path):
                os.makedirs(path)

            file_name = path + filename
            img.save(file_name)

            file_img_url = "http://" + request.META['HTTP_HOST'] + MEDIA_URL + "post/" + filename

            context = {
                'result': "file_uploaded",
                'resultcode': "ok",
                'file_name': file_img_url
            }

        except Exception, e:
            context = {
                'result': e,
                'resultcode': "failed",
            }
            print e

        return TemplateResponse(request, "admin/plugin/ajax_upload_result.html", context)


def avatar_image_upload_handler(request):
    if request.method == "POST":
        try:
            file_img = request.FILES['avatar']
            file_suffix = os.path.splitext(file_img.name)[len(os.path.splitext(file_img.name)) - 1]
            # 检查图片格式
            if file_suffix not in image_type:
                return HttpResponse("请上传正确格式的图片文件")
            filename = uuid.uuid1().__str__() + file_suffix

            # 把头像压缩成90大小
            img = Image.open(file_img)
            img = ThumbnailTool.constrain_len_thumbnail(img, 90)

            path = MEDIA_ROOT + "/avatar/"
            if not os.path.exists(path):
                os.makedirs(path)

            file_name = path + filename
            img.save(file_name)

            file_img_url = "http://" + request.META['HTTP_HOST'] + MEDIA_URL + "avatar/" + filename
            user = request.user
            user.avatar_path = file_img_url
            user.save()

        except Exception, e:
            print e

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))

#####################################分割线###########################################
#保存目录
def update_product_menu(request):
    result = {}
    result['success'] = 0
    result['message'] = '请求方式错误'

    #只接受post
    if request.method == "POST":
        menu = request.POST.get("menu", "")
        pk = request.POST.get("pk", "")

        product = Product.objects.get(id=pk)
        
        product.menu_json = menu
        product.save()

        result['success'] = 1
        result['message'] = '目录更新成功'

    return HttpResponse(json.dumps(result))


    

#保存文档,内容
def update_product_content(request):
    result = {}
    result['success'] = 0
    result['message'] = '请求方式错误'

    #只接受post
    if request.method == "POST":
        menu_id = request.POST.get("menu_id", "")
        product_id = request.POST.get("product_id", "")
        content = request.POST.get("content", "")
        content_type = request.POST.get("content_type", "")

        try:  
            content_obj = Content.objects.get(product_id=product_id, menu_id=menu_id)
            content_obj.content_type = content_type
            content_obj.content = content
            content_obj.save() 
        except Content.DoesNotExist:  
            Content.objects.create(
                menu_id = menu_id,
                product_id = product_id,
                content = content,
                content_type = content_type
            )

        result['success'] = 1
        result['message'] = '内容更新成功'

    return HttpResponse(json.dumps(result))
  
#获取文档,内容
def retrieve_product_content(request):
    result = {}
    result['success'] = 0
    result['message'] = '请求方式错误'
    result['data'] = {}

    #只接受post
    if request.method == "POST":
        menu_id = request.POST.get("menu_id", "")
        product_id = request.POST.get("product_id", "")
      
        try:  
            content_obj = Content.objects.get(product_id=product_id, menu_id=menu_id)
            result['data']['content_type'] = content_obj.content_type
            result['data']['content'] = content_obj.content  
        except Content.DoesNotExist:  
            result['data']['content_type'] = 0
            result['data']['content'] = ''

        result['success'] = 1
        result['message'] = '内容获取成功'

    return HttpResponse(json.dumps(result))
   
# 产品名称列表
class ProductView(ListView):
    template_name = 'admin/product_admin.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            product_list = Product.objects.all()
        else:
            product_list = Product.objects.filter(author_id=user.id).exclude(is_deleted=1)

        return product_list

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        objects, page_range = paginator_tool(pages=page, queryset=self.object_list, display_amount=PERNUM)
        context['page_range'] = page_range
        context['objects'] = objects
        context['is_superuser'] = self.request.user.is_superuser
        
        return context

class DeleteProduct(View):
    def get(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            return HttpResponse(u"请登陆！", status=403)
        # 获取删除的博客ID
        pkey = self.kwargs.get('pk')
        product = Product.objects.filter(author_id=user.id).get(pk=pkey)
        product.is_deleted = 1
        product.save()
        return HttpResponseRedirect('/admin/')

class RestoreProduct(View):
    def get(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            return HttpResponse(u"请登陆！", status=403)
        # 获取删除的博客ID
        pkey = self.kwargs.get('pk')
        product = Product.objects.filter(author_id=user.id).get(pk=pkey)
        product.is_deleted = 0
        product.save()
        return HttpResponseRedirect('/admin/')


class NewProduct(CreateView):
    template_name = 'admin/product_new.html'
    model = Product
    fields = ['name', 'docutype', 'description']

    def get_context_data(self, **kwargs):
        context = super(NewProduct, self).get_context_data(**kwargs)
        context['docutype_list'] = Docutype.objects.filter(is_deleted=0).all()
        return context

#post提交保存
class AddProduct(View):
    def post(self, request):
        user = request.user
        name = request.POST.get("name", "")
        description = request.POST.get("description", "")
        docutype = request.POST.get("docutype", "")
        docutypet_foreignkey = Docutype.objects.get(pk=docutype)

        #创建文档
        post_obj = Product.objects.create(
            name=name,
            author=user,
            docutype=docutypet_foreignkey,
            description=description,
            menu_json = '[{ id:1, pId:0, name:"根目录"},{lastId:2}]'
        )

        return HttpResponseRedirect('/admin/')

#编辑
class ProductUpdate(UpdateView):
    template_name = 'admin/product_update.html'
    model = Product
    fields = ['name', 'docutype', 'description']

    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        context['docutype_list'] = Docutype.objects.all()
        return context


class UpdateProduct(View):
    def post(self, request, *args, **kwargs):

        # 将文件路径和其余信息存入数据库
        name = request.POST.get("name", "")
        description = request.POST.get("description", "")
        docutype = request.POST.get("docutype", "")
        docutypet_foreignkey = Docutype.objects.get(pk=docutype)

        pkey = self.kwargs.get('pk')
        product = Product.objects.get(id=pkey)
        
        product.name = name
        product.description = description
        product.docutype = docutypet_foreignkey
        product.save()

        return HttpResponseRedirect('/admin')


#文档内容 目录编辑页
class ProductMenu(UpdateView):
    template_name = 'admin/content_admin.html'
    model = Product
    fields = ['menu_json']

    def get_context_data(self, **kwargs):
        context = super(ProductMenu, self).get_context_data(**kwargs)

        #查询是否有响应的内容, 默认该文档的根目录
        pkey = self.kwargs.get('pk')

        try:  
            content = Content.objects.get(product_id=pkey, menu_id=1)
            context['content_type'] = content.content_type
            context['content'] = content.content.replace("\n", "<br>").replace('\t','')
        except Content.DoesNotExist:  
            #默认editor编辑器
            context['content_type'] = 0
            context['content'] = ''

        return context


# 文档类型列表
class DocutypeView(ListView):
    template_name = 'admin/docutype_admin.html'
    context_object_name = 'docu_list'

    def get_queryset(self):
        user = self.request.user
        docu_list = Docutype.objects.filter(author_id=user.id).exclude(is_deleted=1)
        return docu_list

    def get_context_data(self, **kwargs):
        context = super(DocutypeView, self).get_context_data(**kwargs)
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        objects, page_range = paginator_tool(pages=page, queryset=self.object_list, display_amount=PERNUM)
        context['page_range'] = page_range
        context['objects'] = objects
        context['editor_list'] = EDITOR
        return context

class DeleteDocutype(View):
    def get(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            return HttpResponse(u"请登陆！", status=403)
        # 获取删除的博客ID
        pkey = self.kwargs.get('pk')
        docutype = Docutype.objects.filter(author_id=user.id).get(pk=pkey)
        docutype.is_deleted = 1
        docutype.save()
        return HttpResponseRedirect('/admin/docutype')


class NewDocutype(CreateView):
    template_name = 'admin/docutype_new.html'
    model = Docutype
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super(NewDocutype, self).get_context_data(**kwargs)
        return context

#post提交保存
class AddDocutype(View):
    def post(self, request):
        # 获取当前用户
        user = request.user
        # 获取评论
        name = request.POST.get("name", "")


        post_obj = Docutype.objects.create(
            name=name,
            author=user,
        )

        return HttpResponseRedirect('/admin/docutype')

#编辑
class DocutypeUpdate(UpdateView):
    template_name = 'admin/docutype_update.html'
    model = Docutype
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super(DocutypeUpdate, self).get_context_data(**kwargs)
        return context


class UpdateDocutype(View):
    def post(self, request, *args, **kwargs):

        # 将文件路径和其余信息存入数据库
        name = request.POST.get("name", "")
        pkey = self.kwargs.get('pk')
        docutype = Docutype.objects.get(id=pkey)
        docutype.name = name
        docutype.save()

        return HttpResponseRedirect('/admin/docutype')


#####################################分割线###########################################
class PostView(ListView):
    template_name = 'admin/blog_admin.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        user = self.request.user
        post_list = Post.objects.filter(author_id=user.id).exclude(status=2)
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        objects, page_range = paginator_tool(pages=page, queryset=self.object_list, display_amount=PERNUM)
        context['page_range'] = page_range
        context['objects'] = objects
        context['editor_list'] = EDITOR
        return context


class DeletePost(View):
    def get(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            return HttpResponse(u"请登陆！", status=403)
        # 获取删除的博客ID
        pkey = self.kwargs.get('pk')
        post = Post.objects.filter(author_id=user.id).get(pk=pkey)
        post.status = 2
        post.save()
        return HttpResponseRedirect('/admin/')


class NewPost(CreateView):
    template_name = 'admin/post_new.html'
    model = Post
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(NewPost, self).get_context_data(**kwargs)
        context['catalogue_list'] = Catalogue.objects.all()
        return context


class UpdatePostIndexView(UpdateView):
    template_name = 'admin/post_new.html'
    model = Post
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(UpdatePostIndexView, self).get_context_data(**kwargs)
        context['catalogue_list'] = Catalogue.objects.all()
        return context


class AddPost(View):
    def post(self, request):
        # 获取当前用户
        user = request.user
        # 获取评论
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        catalogue = request.POST.get("catalogue", "")
        tags = request.POST.getlist("tag", "")
        action = request.POST.get("action", "0")

        catalogue_foreignkey = Catalogue.objects.get(name=catalogue)
        editor_choice = user.editor_choice

        post_obj = Post.objects.create(
            title=title,
            author=user,
            content=content,
            catalogue=catalogue_foreignkey,
            status=action,
            editor_choice=editor_choice,
        )

        post_obj.update_tags(tags)

        return HttpResponseRedirect('/admin/')


class UpdateDraft(View):
    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = request.user
        # 获取要修改的博客
        pkey = self.kwargs.get('pk')
        post = Post.objects.filter(author_id=user.id).get(pk=pkey)
        # 获取评论
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        catalogue = request.POST.get("catalogue", "")
        tags = request.POST.getlist("tag", "")
        action = request.POST.get("action", "0")

        catalogue_foreignkey = Catalogue.objects.get(name=catalogue)

        post.title = title
        post.content = content
        post.catalogue = catalogue_foreignkey
        post.status = action
        post.modify_time = datetime.datetime.now()
        post.save()

        post.update_tags(tags)

        return HttpResponseRedirect('/admin/')


class UpdatePost(View):
    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = request.user
        # 获取要修改的博客
        pkey = self.kwargs.get('pk')
        post = Post.objects.filter(author_id=user.id).get(pk=pkey)
        # 获取评论
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        catalogue = request.POST.get("catalogue", "")
        tags = request.POST.getlist("tag", "")
        action = 1

        catalogue_foreignkey = Catalogue.objects.get(name=catalogue)

        post.title = title
        post.content = content
        post.catalogue = catalogue_foreignkey
        post.status = action
        post.modify_time = datetime.datetime.now()
        post.save()

        post.update_tags(tags)

        return HttpResponseRedirect('/admin/')


class UpdateEditor(View):
    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = request.user

        if not user.is_authenticated():
            return HttpResponse(u"请登陆！", status=403)
        # 获取编辑器
        editor = request.POST.get("editor", "")
        user.editor_choice = editor
        user.save()

        return HttpResponseRedirect('/admin/')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        from django.contrib.auth.views import logout
        return logout(request, next_page='/')


class CarouselIndexView(ListView):
    template_name = 'admin/carousel_admin.html'
    context_object_name = 'carousel_list'
    queryset = Carousel.objects.all()


class CarouselEditView(CreateView):
    template_name = 'admin/carousel_new.html'
    model = Carousel
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(CarouselEditView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(status=1)
        return context


class AddCarousel(View):
    def post(self, request, *args, **kwargs):

        # 将文件路径和其余信息存入数据库
        title = request.POST.get("title", "")
        post = request.POST.get("post", "")
        post_foreignkey = Post.objects.get(pk=post)
        image_link = request.POST.get("image_link", "")

        if not image_link:
            filename = ""
            try:
                file_img = request.FILES['files']
                file_suffix = os.path.splitext(file_img.name)[len(os.path.splitext(file_img.name)) - 1]
                filename = uuid.uuid1().__str__() + file_suffix

                # 把过大的图像压缩成合适的轮播图大小
                img = Image.open(file_img)
                img = ThumbnailTool.constrain_len_thumbnail(img, 865)

                path = MEDIA_ROOT + "/carousel/"
                if not os.path.exists(path):
                    os.makedirs(path)

                file_name = path + filename
                img.save(file_name)
            except Exception, e:
                print e
            file_img_url = "http://" + request.META['HTTP_HOST'] + MEDIA_URL + "carousel/" + filename
            Carousel.objects.create(
                title=title,
                post=post_foreignkey,
                img=file_img_url,
            )
        else:
            Carousel.objects.create(
                title=title,
                post=post_foreignkey,
                img=image_link,
            )
        return HttpResponseRedirect('/admin/carousel')


class DeleteCarousel(View):
    def get(self, request, *args, **kwargs):
        # 获取删除的博客ID
        pkey = self.kwargs.get('pk')
        carousel = Carousel.objects.get(id=pkey)
        carousel.delete()
        return HttpResponseRedirect('/admin/carousel')


class CarouselUpdateView(UpdateView):
    template_name = 'admin/carousel_update.html'
    model = Carousel
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(CarouselUpdateView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        return context


class UpdateCarousel(View):
    def post(self, request, *args, **kwargs):

        # 将文件路径和其余信息存入数据库
        title = request.POST.get("title", "")
        post = request.POST.get("post", "")
        post_foreignkey = Post.objects.get(pk=post)
        image_link = request.POST.get("image_link", "")

        pkey = self.kwargs.get('pk')
        carousel = Carousel.objects.get(id=pkey)

        if not image_link:
            try:
                file_img = request.FILES['files']
                file_suffix = os.path.splitext(file_img.name)[len(os.path.splitext(file_img.name)) - 1]
                filename = uuid.uuid1().__str__() + file_suffix

                # 把过大的图像压缩成合适的轮播图大小
                img = Image.open(file_img)
                img = ThumbnailTool.constrain_len_thumbnail(img, 865)

                path = MEDIA_ROOT + "/carousel/"
                if not os.path.exists(path):
                    os.makedirs(path)

                file_name = path + filename
                img.save(file_name)
            except Exception, e:
                print e
            file_img_url = "http://" + request.META['HTTP_HOST'] + MEDIA_URL + "carousel/" + filename

            carousel.title = title
            carousel.post = post_foreignkey
            carousel.img = file_img_url
            carousel.save()

        else:
            carousel.title = title
            carousel.post = post_foreignkey
            carousel.img = image_link
            carousel.save()
        return HttpResponseRedirect('/admin/carousel')


class UserSetView(ListView):
    template_name = 'admin/userset_admin.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        user_list = User.objects.all()
        return user_list

    def get_context_data(self, **kwargs):
        context = super(UserSetView, self).get_context_data(**kwargs)
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        objects, page_range = paginator_tool(pages=page, queryset=self.object_list, display_amount=PERNUM)
        context['page_range'] = page_range
        context['objects'] = objects
        return context


class NewUserView(CreateView):
    template_name = 'admin/userset_new.html'
    model = User
    fields = ['username']


class AddUser(View):
    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        name = request.POST.get("name", "")
        email = request.POST.getlist("email", "")

        user_obj = User.objects.create_user(
            username="".join(username),
            password="".join(password),
            email="".join(email),
        )

        user_obj.name = name
        user_obj.is_superuser = 0
        user_obj.is_staff = 1

        user_obj.save()

        return HttpResponseRedirect('/admin/user')


class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            return HttpResponse(u"请登陆！", status=403)

        # 获取删除的博客ID
        pkey = self.kwargs.get('pk')
        User.objects.get(pk=pkey).delete()

        #刷新页面
        return HttpResponseRedirect('/admin/user')

#编辑
class UserUpdate(UpdateView):
    template_name = 'admin/userset_update.html'
    model = User
    fields = ['name', 'username', 'email']

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        return context


class UpdateUser(View):
    def post(self, request, *args, **kwargs):
        # 获取当前用户
        user = self.request.user
        # 判断当前用户是否是活动的用户
        if not user.is_authenticated():
            return HttpResponse(u"请登陆！", status=403)


        # 将文件路径和其余信息存入数据库
        username = request.POST.get("username", "")
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        is_pwd_reset = request.POST.get("is_pwd_reset", "")
        pwd = request.POST.get("password", "")
        
        pkey = self.kwargs.get('pk')
        user_obj = User.objects.get(id=pkey)

        if is_pwd_reset:
            user_obj.set_password(pwd)
        
        user_obj.name = name
        user_obj.email = email
        user_obj.username = username
        user_obj.save()

        return HttpResponseRedirect('/admin/user')
