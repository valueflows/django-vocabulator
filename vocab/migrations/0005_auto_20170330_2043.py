# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0004_auto_20170330_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentrelationshiprole',
            name='label',
            field=models.CharField(default='', max_length=255, verbose_name='label'),
            preserve_default=False,
        ),
    ]