# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_controller', '0005_app_version_appstore_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_version',
            name='company',
            field=models.CharField(max_length=30, null=True, verbose_name='\u516c\u53f8', blank=True),
        ),
    ]
