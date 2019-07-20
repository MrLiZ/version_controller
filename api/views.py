#! /usr/bin/env python
# coding:utf-8

from rest_framework.views import APIView
from rest_framework.response import Response

from app_controller.models import *
import aliyun_oss2.backends

class UploadAPP(APIView):
    """
    上传app接口处理
    使用curl上传:
    curl -H "Accept: application/json; indet=4" -F "project_brief=xxx" -F "ipa=@xxx.ipa" -F "apk=@xxx.apk" -u admin:admin http://127.0.0.1:8000/api/upload_app/
    """

    def post(self, request, format=None):

        project_brief = request.data["project_brief"] if 'project_brief' in request.data else None   # 项目简称
        ipa = request.data["ipa"] if 'ipa' in request.data else None   # ipa
        apk = request.data["apk"] if 'apk' in request.data else None  # apk

        if project_brief == "prod":
            return Response({"status": 0, "message": u"不能上传正式环境安装包!"})

        try:
            project = Project.objects.get(brief=project_brief)
        except Project.DoesNotExist:
            project = Project.objects.create(name=project_brief, brief=project_brief)

        app = App_Version(project=project, ipa=ipa, apk=apk)
        app.save()
        aliyun_oss2.backends.upload_to_oss2(app)

        return Response({"status": 1, "message": u"上传成功!"})