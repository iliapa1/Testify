# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-02 20:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000)),
                ('a_num', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='one',
            name='o_question',
        ),
        migrations.RemoveField(
            model_name='test',
            name='a_num',
        ),
        migrations.RemoveField(
            model_name='test',
            name='q_num',
        ),
        migrations.DeleteModel(
            name='One',
        ),
        migrations.AddField(
            model_name='questions',
            name='T_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Test'),
        ),
        migrations.AddField(
            model_name='answers',
            name='q_answers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Questions'),
        ),
    ]