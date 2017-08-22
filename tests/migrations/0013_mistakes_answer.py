# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 12:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0012_mistakes'),
    ]

    operations = [
        migrations.AddField(
            model_name='mistakes',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Answers'),
            preserve_default=False,
        ),
    ]