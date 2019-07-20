# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_controller', '0002_auto_20160922_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_version',
            name='ipa_plist',
            field=models.FileField(upload_to=b'ios/', null=True, verbose_name='ipa plist\u6587\u4ef6', blank=True),
        ),
        migrations.AddField(
            model_name='app_version',
            name='ipa_title',
            field=models.CharField(default=b'', max_length=30, null=True, verbose_name='\u5e94\u7528title', blank=True),
        ),
    ]
