from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate
from django.core.urlresolvers import reverse
from .forms import ChangeUserInfoForm
from .models import UserInfo

# Create your views here.

# 主页
def home_page(request):
    return render(request, 'home.html',
                  # {'form': ItemForm()}
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
        userinfo = UserInfo.objects.get(belong_to__username="thejojo")
        userinfo.age = age
        userinfo.address = address
        userinfo.save()
        # if form.is_valid():
            # userinfo.save()
        return HttpResponseRedirect(reverse('lists:userinfo'))
    return render(request, 'registration/userinfo.html',{"form":form})
