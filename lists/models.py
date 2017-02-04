from django.db import models
from django.contrib.auth.models import User
# Create your models here.




# UserInfo
class UserInfo(models.Model):
    # 一对一，一条信息，对应一个人
    # related_name是反向关联
    belong_to = models.OneToOneField(to=User, related_name='info',)

    # 添加要扩展到 User 中的新字段
    age = models.IntegerField("年龄",default=20, blank=False, name = "age")
    address = models.CharField("地址",max_length=50, default="中国", blank=False)

    def __str__(self):

        return self.belong_to.username


