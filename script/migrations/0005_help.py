# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-24 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script', '0004_auto_20181124_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.TextField(unique=True)),
                ('explain', models.TextField()),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
