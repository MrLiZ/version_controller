# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app_controller.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_controller', '0003_auto_20160926_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_version',
            name='ipa',
            field=models.FileField(upload_to=app_controller.models.upload_ipa, null=True, verbose_name='ipa\u6587\u4ef6', blank=True),
        ),
    ]
