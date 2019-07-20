# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_controller', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='brief',
            field=models.CharField(default=b'', unique=True, max_length=30, verbose_name='\u5e94\u7528\u7b80\u79f0'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default=b'', unique=True, max_length=30, verbose_name='\u5e94\u7528\u540d\u79f0'),
        ),
    ]
