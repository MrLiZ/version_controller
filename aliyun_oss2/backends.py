# -*- coding: utf-8 -*-
import os

import oss2
from version_controller.settings import ACCESS_KEY_ID, ACCESS_KEY_SECRET, END_POINT, BUCKET_NAME, ALIYUN_OSS_CNAME


# 上传文件到OSS2
def upload_to_oss2(instance):
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, END_POINT, BUCKET_NAME)

    # 上传apk
    if instance.apk:
        with open(instance.apk.path) as apk:
            # 去掉链接前面的/
            bucket.put_object(instance.apk.url[1:], apk)
        os.remove(instance.apk.path)

    # 上传ipa和plist
    if instance.ipa:
        with open(instance.ipa.path) as ipa:
            # 去掉链接前面的/
            bucket.put_object(instance.ipa.url[1:], ipa)
        os.remove(instance.ipa.path)
        with open(instance.ipa_plist.path) as ipa_plist:
            # 去掉链接前面的/
            bucket.put_object(instance.ipa_plist.url[1:], ipa_plist)
        os.remove(instance.ipa_plist.path)


# 从OSS2删除文件
def delete_from_oss2(file):
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, END_POINT, BUCKET_NAME)
    # 去掉链接前面的/
    bucket.delete_object(file[1:])
