# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_dd_node_dd_poly'),
    ]

    operations = [
        migrations.CreateModel(
            name='userInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
            ],
        ),
    ]
