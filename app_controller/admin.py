#! /usr/bin/env python
# coding:utf-8
from django.contrib import admin

from models import *
import aliyun_oss2.backends

# Register your models here.


class AppVersionInline(admin.TabularInline):
    model = App_Version
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [AppVersionInline]

    # 重写admin的保存方法,保存的时候把安装包上传到OSS,避免mysql被锁住
    def change_view(self, request, object_id):

        result = super(ProjectAdmin, self).change_view(request, object_id)

        # 上传文件的时候保存到OSS
        if request.method == "POST" and len(request._files) > 0:
            app = App_Version.objects.filter(project__id=object_id)[0]
            aliyun_oss2.backends.upload_to_oss2(app)

        return result

@admin.register(App_Version)
class AppVersionAdmin(admin.ModelAdmin):
    pass