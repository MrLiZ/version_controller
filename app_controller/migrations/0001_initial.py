# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App_Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ipa', models.FileField(upload_to=b'ios/', null=True, verbose_name='ipa\u6587\u4ef6', blank=True)),
                ('ipa_version', models.CharField(max_length=30, null=True, verbose_name='ios\u7248\u672c', blank=True)),
                ('ipa_build', models.CharField(max_length=30, null=True, verbose_name='ios Build', blank=True)),
                ('ipa_size', models.DecimalField(null=True, verbose_name='ipa\u6587\u4ef6\u5927\u5c0f/M', max_digits=6, decimal_places=3, blank=True)),
                ('ipa_bundleid', models.CharField(max_length=100, null=True, verbose_name='ipa Bundle ID', blank=True)),
                ('apk', models.FileField(upload_to=b'android/', null=True, verbose_name='apk\u6587\u4ef6', blank=True)),
                ('apk_version', models.CharField(max_length=30, null=True, verbose_name='android\u7248\u672c', blank=True)),
                ('apk_build', models.CharField(max_length=30, null=True, verbose_name='android Build', blank=True)),
                ('apk_size', models.DecimalField(null=True, verbose_name='apk\u6587\u4ef6\u5927\u5c0f/M', max_digits=6, decimal_places=3, blank=True)),
                ('apk_bundleid', models.CharField(max_length=100, null=True, verbose_name='apk Bundle ID', blank=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_time', models.DateTimeField(auto_now_add=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-last_time'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=30, verbose_name='\u5e94\u7528\u540d\u79f0')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_time', models.DateTimeField(auto_now_add=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
        ),
        migrations.AddField(
            model_name='app_version',
            name='project',
            field=models.ForeignKey(verbose_name='\u5e94\u7528', to='app_controller.Project'),
        ),
    ]
