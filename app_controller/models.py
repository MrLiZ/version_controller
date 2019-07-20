#! /usr/bin/env python
# coding:utf-8
import datetime
import os

from django.db import models
from django.core.files import File

from utils import *
import aliyun_oss2.backends

# Create your models here.


class Project(models.Model):
    # 自定义名称
    name = models.CharField(max_length=30, null=False, blank=False, default='', verbose_name=u"应用名称", unique=True)
    # 自定义简称
    brief = models.CharField(max_length=30, null=False, blank=False, default='', verbose_name=u"应用简称", unique=True)
    # 公司名称,可以根据不同公司跳转不同下载页面
    company = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"公司")

    created_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    last_time = models.DateTimeField(verbose_name=u"更新时间", auto_now_add=True)

    def __unicode__(self):
        return self.name


def upload_ipa(instance, filename):

    return 'ios/{0}'.format(get_file_name(instance.project.brief, filename))


def upload_plist(instance, filename):
    return '{0}{1}'.format(instance.ipa.name[:-4], ".plist")


def upload_apk(instance, filename):

    return 'android/{0}'.format(get_file_name(instance.project.brief, filename))


class App_Version(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"应用")

    # 不能是中文名
    ipa = models.FileField(upload_to=upload_ipa, verbose_name=u"ipa文件", blank=True, null=True)
    ipa_version = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"ios版本")
    ipa_build = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"ios Build")
    ipa_size = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, verbose_name=u"ipa文件大小/M")
    ipa_bundleid = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"ipa Bundle ID")
    # 打包时设置的应用名称,用于plist文件,不能是中文名
    ipa_title = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name=u"应用title")
    ipa_plist = models.FileField(upload_to=upload_plist, verbose_name=u"ipa plist文件", blank=True, null=True)
    appstore_url = models.URLField(verbose_name=u"AppStore链接", blank=True, null=True)

    apk = models.FileField(upload_to=upload_apk, verbose_name=u"apk文件", blank=True, null=True)
    apk_version = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"android版本")
    apk_build = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"android Build")
    apk_size = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, verbose_name=u"apk文件大小/M")
    apk_bundleid = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"apk Bundle ID")

    created_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    last_time = models.DateTimeField(verbose_name=u"更新时间", auto_now_add=True)

    def __unicode__(self):
        return self.project.name + "-" + self.ipa_version

    class Meta:
        ordering = ['-last_time']

    def save(self, *args, **kwargs):
        super(App_Version, self).save(*args, **kwargs)
        if self.apk:
            self.apk_size, self.apk_version, self.apk_build, self.apk_bundleid = analysis_apk(self.apk.path)
        if self.ipa:
            self.ipa_size, self.ipa_version, self.ipa_build, self.ipa_bundleid, self.ipa_title = analysis_ipa(self.ipa.path)
            plist = create_plist(self)
            with open(plist, 'r') as f:
                self.ipa_plist = File(f)
                super(App_Version, self).save(*args, **kwargs)
            os.remove(plist)
        super(App_Version, self).save(*args, **kwargs)
        # aliyun_oss2.backends.upload_to_oss2(self)


# 删除对象时删除文件
def on_delete(sender, instance, **kwargs):
    # 老的存在本地的apk文件删除
    if instance.apk and judge_old_app(instance.apk.url):
        try:
            os.remove(get_old_app_path(instance.apk.path))
        except OSError:
            pass
        # instance.apk.delete(save=False)
    # 阿里云OSS文件删除
    elif instance.apk:
        aliyun_oss2.backends.delete_from_oss2(instance.apk.url)

    # 老的存在本地的ipa文件删除
    if instance.ipa and judge_old_app(instance.ipa.url):
        try:
            os.remove(get_old_app_path(instance.ipa.path))
        except OSError:
            pass
        # instance.ipa.delete(save=False)
    # 阿里云OSS文件删除
    elif instance.ipa:
        aliyun_oss2.backends.delete_from_oss2(instance.ipa.url)

    # 老的存在本地的ipa_plist文件删除
    if instance.ipa_plist and judge_old_app(instance.ipa_plist.url):
        try:
            os.remove(get_old_app_path(instance.ipa_plist.path))
        except OSError:
            pass
        # instance.ipa_plist.delete(save=False)
    # 阿里云OSS文件删除
    elif instance.ipa_plist:
        aliyun_oss2.backends.delete_from_oss2(instance.ipa_plist.url)

models.signals.post_delete.connect(on_delete, sender=App_Version)
