# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-06 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0015_messenger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userSender', models.CharField(max_length=100)),
                ('userReciever', models.CharField(max_length=100)),
                ('stateOfRequest', models.CharField(max_length=100)),
            ],
        ),
    ]
