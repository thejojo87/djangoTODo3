from django.contrib import admin
from .models import UserInfo,Item
# Register your models here.


# admin.site.register()

class ItemAdmin(admin.ModelAdmin):
    list_display = ('text','belong_to',)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('belong_to','age','address',)

admin.site.register(Item,ItemAdmin)
admin.site.register(UserInfo,UserInfoAdmin)

