# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-27 10:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_auto_20171026_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='desc',
            field=models.TextField(default=1, verbose_name='Description'),
            preserve_default=False,
        ),
    ]