# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 08:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0003_userinput'),
    ]

    operations = [
        migrations.AddField(
            model_name='dd_node',
            name='session',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
