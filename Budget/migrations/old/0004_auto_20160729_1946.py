# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-29 17:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Budget', '0003_auto_20160729_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 29, 19, 46, 28, 507682)),
        ),
    ]
