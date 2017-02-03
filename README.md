# DjangoToDo

[TOC]

# 资源
Django +python3.6 +win10 +mysql

参考的书：python web 测试驱动方法

http://www.obeythetestinggoat.com/pages/book.html#toc

https://github.com/hjwp/book-example


# 目标
我想要做什么？
Django做的一个ToDo网站。
用户登陆功能。
RestfulAPI
Swift写个iphone客户端。

发布。




# 遇到的问题

## 问题1：selenuim3无法运行
最开始的测试，因为selenium3需要一个geckodriver的驱动。

https://www.zhihu.com/question/49568096

https://github.com/mozilla/geckodriver/releases

下载这个驱动，放在firefox安装目录，并且系统变量里添加firefox目录就可以了。

## 问题2：pycharm运行runserver，会有exit

Process finished with exit code -1073741819 (0xC0000005)
这个是因为run错了。
pycharm，run configuration里有Django server，而不是像之前一样的python里，添加manage。

## 问题3：Django url引用出错。

django1.10开始修改了地址引用方式。
需要直接在上面引用，然后下面是变量，而不是string

http://stackoverflow.com/questions/38744285/django-urls-error-view-must-be-a-callable-or-a-list-tuple-in-the-case-of-includ

## 问题4：runserver后台怎么运行？
直接后面加一个& 就可以了。
但是后台运行就就不太好杀了。
端口会表示占用的。
只好用nginx重启方式了。
sudo service nginx reload

    You can use netstat -tulpn to see the PID
    kill -9 PID

## 问题5： upstart已经被淘汰了。systemd
怎么转换？

https://gist.github.com/marcanuy/5ae0e0ef5976aa4a10a7

http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html

https://piaosanlang.gitbooks.io/spiders/content/05day/section5.4.html


## 问题6： 数据库进入方法

cd C:\Program Files\MySQL\MySQL Server 5.7\bin
mysql -u root -p thejojo

# 总结

# 项目进度

# Day1

新建一个django
startapp lists
修改setting-添加数据库，创建数据库database
root thejojo
设置static_root

先做个主页
去url，设置一下
因为要从lists引用太多views里的函数。
所以使用include方法。

然后从lists里import views，以后引用的时候很方便。

```python
from django.conf.urls import url,include
from django.contrib import admin
from lists import views as lists_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', lists_views.home_page, name="home"),
]
```

然后去lists/views.py新建一个home_page函数。
最简单的就可以。

```python
def home_page(request):
    return render(request,'home.html')
```

mysql链接需要安装pymysql
然后在lists项目的init文件里添加下面两行

import pymysql
pymysql.install_as_MySQLdb()

然后启动admin后台。
admin需要在数据库生成table。
所以需要migrate命令
python manage.py createsuperuser
这个用来创造管理员。


下一步就是主页了。

新建一个base文件。
再建一个navbar，放进base里
最后建一个home文件。

最后替换掉原来的view函数就可以了。


