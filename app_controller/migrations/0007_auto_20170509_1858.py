# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_controller', '0006_app_version_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app_version',
            name='company',
        ),
        migrations.AddField(
            model_name='project',
            name='company',
            field=models.CharField(max_length=30, null=True, verbose_name='\u516c\u53f8', blank=True),
        ),
    ]
