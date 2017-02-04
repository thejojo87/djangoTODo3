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

忘了做git了。
1. git init
2. git remote add origin https://github.com/thejojo87/djangoTODo3.git
3. git add.
4. git commit -m "Day1"
5. git push origin master

## 用户系统-login

系统自带用户系统，如果新建一个那就是重复造轮子了。
还需要验证等等，虽然不复杂，但有点麻烦。
那就用原来的系统吧。

### 1.添加url

先注册lists/url.py文件

```python
url(r'^lists/',include('lists.urls',namespace="lists")),
```
然后注册lists/url.py文件
```python
url(r'^accounts/',include('django.contrib.auth.urls')),
```
这一行，会添加一系列的网址。

### 2.写registration/login.html
因为用户自带了login系统。
所以login view函数是没必要写的。

只需要写html文件就可以了。

view函数里要注册的form是AuthenticationForm类。

样式如果按照bootstrap和javascript和jquery，应该能做个很漂亮的。
以后再学。
现在先做个最简单的表格。

如果有error，那么就显示。

## 用户系统-注册

### 1.先添加url

```python
url(r'^accounts/register', list_views.register_page, name="register"),
```

### 2.写register函数

```python
# 注册页面
def register_page(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            # return HttpResponseRedirect('/')
            return HttpResponseRedirect(reverse('home'))
    context['form'] = form
    return render(request,'registration/register.html',context)
```

### 3.写register的html文件

写完就结束了。
到目前为止实现了，用户的注册。

# Day2
## 用户系统-用户信息模块

想达到的效果是，点击登陆navbar里的用户账号，就可以转入用户信息模块。
用户信息应该可以修改。

### 1.写url

```python
 url(r'^accounts/userinfo',userinfo, name="userinfo"),
```

### 2.新建一个UserInfoModel
django允许你使用Form变形 ModelForm 类为任何 Model类或实例取得一个Form子类，
一个ModelForm和普通Form基本一样，但是包含了一个Meta嵌套类（类似Model里的Meta），内含一个必须的属性 model

举个例子：

```python
from django import newforms as forms

class PersonForm(forms.Form):
    first = forms.CharField(max_length=100, required=True)
    last = forms.CharField(max_length=100, required=True)
    middle = forms.CharField(max_length=100)

from django import newforms as forms
from mysite.myapp.models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
```

也就是说，与其盲目建个表格，还不如先建数据模型。


```python
class UserInfo(models.Model):
    # 一对一，一条信息，对应一个人
    # related_name是反向关联
    belong_to = models.OneToOneField(to=User, related_name='info')

    # 添加要扩展到 User 中的新字段
    age = models.IntegerField("年龄",null=True, blank=True)
    address = models.CharField("地址",max_length=50, null=True, blank=True)

    def __str__(self):
        return self.belong_to.username
```

然后为了在后台能监控，在admin里添加。

```python
from .models import UserInfo
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('belong_to','age','address',)

admin.site.register(UserInfo,UserInfoAdmin)
```

### 3.新建一个UserInfoForm

这次需要传递并且修改userinfo，所以需要一个form。
新建一个forms.py文件

创建用于修改用户信息的form模型。
一共有三个属性，属于，年龄和地址。
其中属于应该无法更改。


```python
class ChangeUserInfoForm(forms.models.ModelForm):

    class Meta:
        model = UserInfo
        fields = ('age','address')
        # widgets = {
        #     'age':forms.fields.NumberInput(attrs={
        #         'class': 'form-control input-lg'
        #     }),
        # }
        error_messages = {
            'belong_to': {'required':Cannot_change_belongto}
        }
    def save(self, commit=True):
        print("form saved")
```

### 4.写view函数

思路就是，如果是get的时候，那么就新建一个字典。
来初始化userinfoform表格。把这个传递过去。

如果是post，那么就验证保存。
主要是得检查重复。
先查找数据库里，名字是request.user.username一样的用户。
然后是保存。

在form.save方法里。
就是修改userinfo信息。

```python
def userinfo(request):
    if request.method == 'GET':
        data = {'belong_to':request.user.username, 'age':request.user.info.age, 'address':request.user.info.address}
        form = ChangeUserInfoForm(data)
    else:
        form = ChangeUserInfoForm(request.POST)
        age = request.POST['age']
        address = request.POST['address']
        userinfo = UserInfo.objects.get(belong_to__username="thejojo")
        userinfo.age = age
        userinfo.address = address
        userinfo.save()
        # if form.is_valid():
            # userinfo.save()
        return HttpResponseRedirect(reverse('lists:userinfo'))
    return render(request, 'registration/userinfo.html',{"form":form})
```

做完了用户信息模块。

但是重复检测，并没有做到。




