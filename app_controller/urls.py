#! /usr/bin/env python
# coding:utf-8

from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^(?P<brief>.+)/(?P<version>.+)/$', views.app_download, name='app-download'),
    url(r'^(?P<brief>.+)/$', views.app_download, name='latest-app-download'),
]