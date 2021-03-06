# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-26 21:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='One',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000)),
                ('answers', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('q_num', models.CharField(max_length=100)),
                ('a_num', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='one',
            name='o_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Test'),
        ),
    ]
