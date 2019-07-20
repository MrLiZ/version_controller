# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app_controller.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_controller', '0007_auto_20170509_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_version',
            name='apk',
            field=models.FileField(upload_to=app_controller.models.upload_apk, null=True, verbose_name='apk\u6587\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='app_version',
            name='ipa_plist',
            field=models.FileField(upload_to=app_controller.models.upload_plist, null=True, verbose_name='ipa plist\u6587\u4ef6', blank=True),
        ),
    ]
