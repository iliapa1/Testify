# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-10 15:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0007_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='answer_r',
            field=models.CharField(default=django.utils.timezone.now, max_length=1000),
            preserve_default=False,
        ),
    ]
