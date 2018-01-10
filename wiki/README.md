## 目录
在别人的基础上简单开发个文档系统，使用ztree, ueditor, markdown插件


需要安装的包：
django
django-tagging
pillow(该包为PIL的一个分支，目前pip和easy_install好像都无法下载安装PIL了)
MySQL-python（还有一个数据库驱动，我使用的是MySQL，你也可以使用其他驱动）

安装完成后，打开 zer0Blog/settings，修改其中的数据库配置。配置如下：

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'zer0Blog',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': '127.0.0.1',
            'PORT': '3306'
        }
    }

若使用MySQL，则需要修改 `USER` ,`PASSWORD`,`HOST` 和你想使用的数据库名 `NAME`。若使用其他数据库，还需要修改 `ENGINE'。熟悉 Django 的都知道怎么做，就不细说了

然后就是在项目根目录下输入 `python manager.py makemigrations` ，再输入 `python manager.py migrate` 生成数据库表。然后使用 `python manager.py runserver` 启动数据库即可。

一个要点:`管理员账户必须使用 python manager.py createsuperuser 命令来创建`

若要正式部署使用，建议使用 nginx+uwsgi 部署，可参考[Nginx+uWSGI安装与配置](http://mdba.cn/?p=109)


部署过程：
1. 检查python版本 2.7
2. 创建项目wiki.qingsonglaoban.com,将项目文件复制上去
3. 安装 pip install django==1.9.13 PyMySQL django-tagging pillow（pip可能需要更新：pip install --upgrade pip）
4. setting中修改数据库配置， 删除mwiki\blog\migrations中的文件只剩下init.py
5. 初始化数据库
	python manage.py makemigrations 
	python manage.py migrate
6. 创建超级管理员 python manage.py createsuperuser， 账号admin 密码qslb2018
7. 运行服务器 python manage.py runserver 0.0.0.0:8090

8. 若有nginx部署
	- pip install uwsgi (centos7报错就运行下：yum install python-devel)
	- centos下的坑 http://www.linuxidc.com/Linux/2016-10/135743p3.htm
9. 复制静态文件：
    - STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    - python manage.py collectstatic

uwsgi参考：

[uwsgi]

env = DJANGO_PRODUCTION_SETTINGS=TRUE

chdir = /home/wiki.qingsonglaoban.com
module = zer0Blog.wsgi

master=True
processes = 4
http = :8091
vaccum=True
socket = 127.0.0.1:8092
touch-reload = /home/wiki.qingsonglaoban.com
daemonize = /var/log/uwsgi.log