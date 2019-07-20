# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_controller', '0004_auto_20160926_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_version',
            name='appstore_url',
            field=models.URLField(null=True, verbose_name='AppStore\u94fe\u63a5', blank=True),
        ),
    ]
