#! /usr/bin/env python
# coding:utf-8
import json

from django.shortcuts import render, render_to_response, redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from models import *
from utils import *
from version_controller.settings import HTTPS_DOMAIN, ALIYUN_OSS_CNAME


# Create your views here.

def app_download(request, brief, version=None):

    def get_apk_url():
        """
        获取apk的下载链接
        :return: apk的下载链接或者""
        """

        if app.apk and judge_old_app(app.apk.url):
            # 老的安装包放本地的链接
            return "http://" + request.META["HTTP_HOST"] + get_old_app_path(app.apk.url)
        elif app.apk:
            # 阿里云OSS链接
            return ALIYUN_OSS_CNAME + app.apk.url
        else:
            return ""

    def get_ios_url():
        """
        获取ios的下载链接
        :return: ios的下载链接或者""
        """

        if app.appstore_url:
            # AppStore链接
            return app.appstore_url
        elif app.ipa_plist and judge_old_app(app.ipa_plist.url):
            # 老的安装包放本地的链接
            return "itms-services://?action=download-manifest&url=" + HTTPS_DOMAIN + get_old_app_path(app.ipa_plist.url)
        elif app.ipa_plist:
            # 阿里云OSS链接
            return "itms-services://?action=download-manifest&url=" + ALIYUN_OSS_CNAME + app.ipa_plist.url
        else:
            return ""

    def return_render(template):
        """
        响应请求
        :param template: 模板
        :param options: 选项 message（提示内容） apk_url（apk下载链接）  ios_url（ios下载链接）
        :return:
        """
        return render(request, template, options)

    if request.method == "GET":

        options = {
            "message": "",
            "apk_url": "",
            "ios_url": ""
        }

        # 下载最新版本
        if not version:
            apps = App_Version.objects.filter(project__brief=brief)
            app = apps.order_by("-id")[0] if apps.exists() else None
        else:
            apps = App_Version.objects.filter(project__brief=brief, apk_version=version, ipa_version=version)
            app = apps.order_by("-id")[0] if apps.exists() else None

        if not app:
            options["message"] = u"该版本不存在!"
            options["apk_url"] = ""
            options["ios_url"] = ""
        else:
            options["message"] = ""
            options["apk_url"] = get_apk_url()
            options["ios_url"] = get_ios_url()

        # 如果是安卓app更新下载,直接返回下载链接
        if request.GET.get("update_download", 0):
            return redirect(options["apk_url"])

        return return_render("app_download/app_download.html")
