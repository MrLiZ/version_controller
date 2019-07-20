#! /usr/bin/env python
# coding:utf-8

from django.conf.urls import include, url
from rest_framework import routers

import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^upload_app/$', views.UploadAPP.as_view()),    # 上传app接口
]