#! /usr/bin/env python
# coding:utf-8

import os
import commands
import re
import biplist
import datetime

from django.shortcuts import _get_queryset

from version_controller.settings import AAPT, DOMAIN, ALIYUN_OSS_CNAME


def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object, or raises a Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_file_size(file):
    return float(os.path.getsize(file))/1024/1024


def xml_to_dict(xml):
    if xml[0:5].upper() != "<?XML":
        return None

    result = {}
    contents = xml.strip().split('\n')[2:]

    for content in contents:
        pattern_key = re.match(r'\s*<key>(.+)</key>', content)
        if not pattern_key:
            continue

        index = contents.index(content)
        pattern_string = re.match(r'\s*<string>(.+)</string>', contents[index+1])

        if not pattern_string:
            continue

        key = pattern_key.group(1)
        string = pattern_string.group(1)
        result[key] = string

    return result


def analysis_apk(apk):
    size = get_file_size(apk)

    command = AAPT + " dump badging " + apk
    data = {}
    for i in commands.getstatusoutput(command)[1].split("\n")[0].split(" ")[1:]:
        info = i.split("=")
        data[info[0]] = info[1].split("'")[1]

    try:
        return size, data["versionName"], data["versionCode"], data["name"]
    except Exception:
        return 0, '', '', ''


def analysis_ipa(ipa):
    size = get_file_size(ipa)

    zip_file = ipa[:-4] + ".zip"
    command = "cp " + ipa + " " + zip_file + " && unzip " + zip_file + " -d " + zip_file[:-4]
    os.system(command)
    plist_file = zip_file[:-4] + "/Payload/" + commands.getstatusoutput("ls " + zip_file[:-4] + "/Payload/")[1] + "/Info.plist"

    # 解析plist文件
    data = biplist.readPlist(plist_file)

    title = commands.getstatusoutput("ls " + zip_file[:-4] + "/Payload/")[1][:-4]

    rm_command = "rm -rf " + zip_file + " " + zip_file[:-4]
    os.system(rm_command)

    return size, data["CFBundleShortVersionString"], data["CFBundleVersion"], data["CFBundleIdentifier"], title


def create_plist(instance):
    """生成下载安装ipa文件的plist文件
    """

    plist = {
        'items': [{
            'assets': [{
                'kind': 'software-package',
                'url': ALIYUN_OSS_CNAME + instance.ipa.url
            }],
            'metadata': {
                'bundle-identifier': instance.ipa_bundleid,
                'bundle-version': instance.ipa_version,
                'kind': 'software',
                'title': instance.ipa_title
            }
        }]
   }

    file_name = instance.ipa.path[:-4] + ".plist"

    # 生成下载需要的plist文件
    biplist.writePlist(plist, file_name, False)

    return file_name


def judge_old_app(url):
    """
    判断是否是放在本地的安装包
    :param url:  安装包相对路径
    :return:
    """

    # 如果路径为/apps/ios/xxx或者/apps/android/xxx则为放在本地的安装包
    return len(url.split("/")) == 4


def get_old_app_path(path):
    """
    获取放在本地的安装包路径
    :param path:  安装包路径
    :return: 路径
    """
    return path.replace("/apps/", "/media/")


def get_file_name(brief, filename):
    """
    获取保存安装包时的路径和文件名
    :param brief: 应用简称
    :param filename: 应用上传时的文件名,规范: sesame.版本号.apk sesame.版本号.ipa  例如:sesame.1.0.65.0.apk
    :return: 返回包含相对路径的文件名
    """

    time_now = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    filename_list = filename.split(".")

    if len(filename_list) != 6:
        # 如果没有按照规范命名文件,保存为: 下载的简称/时间(精确到秒)/helios.下载的简称.时间(精确到秒).apk(ipa)

        return "{0}/{1}/sesame.{0}.{1}.{2}".format(brief, time_now, filename_list[-1])
    else:
        # 如果按照规范命名,保存为: 下载的简称/时间(精确到秒)/helios.下载的简称.版本号.时间(精确到秒).apk(ipa)

        return "{0}/{1}/sesame.{0}.{2}.{1}.{3}".format(brief, time_now, ".".join(filename_list[1:4]),filename_list[-1])
