from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate
from django.core.urlresolvers import reverse
from .forms import ChangeUserInfoForm,ItemForm,ItemListForm
from .models import UserInfo,Item
from django.contrib.auth.models import User

# Create your views here.

# 主页
def home_page(request):
    if request.user.username != "":
        # 用户登陆了
        Item_ = Item.objects.filter(belong_to__username=request.user.username)
        return render(request, 'home.html',
                  {'form': ItemForm(),'ItemList':Item_}
                  )
    else:
        return render(request, 'home.html',
                  {'form': ItemForm()}
                  )

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

# 用户信息
def userinfo(request):
    if request.method == 'GET':
        data = {'belong_to':request.user.username, 'age':request.user.info.age, 'address':request.user.info.address}
        form = ChangeUserInfoForm(data)
    else:
        form = ChangeUserInfoForm(request.POST)
        age = request.POST['age']
        address = request.POST['address']
        userinfo = UserInfo.objects.get(belong_to__username=request.user.username)
        userinfo.age = age
        userinfo.address = address
        userinfo.save()
        # if form.is_valid():
            # userinfo.save()
        return HttpResponseRedirect(reverse('lists:userinfo'))
    return render(request, 'registration/userinfo.html',{"form":form})

# 新建item的POST请求，并不指向特定页面，实现数据后转到home
def new_item(request):
    if request.user.username != "":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.belong_to = User.objects.get(username=request.user.username)
            user.text = request.POST['text']
            user.save()
    return HttpResponseRedirect(reverse('home'))

# 删除的POST请求，并不指向特定页面
def delete_item(request,id):
    item_to_delete = get_object_or_404(Item,pk=int(id))
    item_to_delete.delete()
    return HttpResponseRedirect(reverse('home'))

# 修改Item，如果是get那么指向修改的html，如果是post就运算
def update_item(request,id):
    item_to_update = get_object_or_404(Item,pk=int(id))
    data = {'belong_to': request.user.username, 'text': item_to_update.text}
    form = ItemForm(data)
    print(form)
    if request.method == "POST":
        item_to_update.text = request.POST['text']
        item_to_update.save()
        return HttpResponseRedirect(reverse('home'))
    return render(request,'registration/update.html',{"form":form, "Item":item_to_update})
