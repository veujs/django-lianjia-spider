# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2019-01-22 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HouseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('house', models.CharField(max_length=20, verbose_name='小区')),
                ('bedroom', models.CharField(max_length=20, verbose_name='房厅')),
                ('area', models.CharField(max_length=20, verbose_name='面积')),
                ('direction', models.CharField(max_length=20, verbose_name='朝向')),
                ('floor', models.CharField(max_length=20, verbose_name='楼层')),
                ('year', models.CharField(max_length=20, verbose_name='年份')),
                ('location', models.CharField(max_length=20, verbose_name='位置')),
                ('total_price', models.IntegerField(verbose_name='总价')),
                ('unit_price', models.IntegerField(verbose_name='单价')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='修改日期')),
            ],
            options={
                'verbose_name': '二手房',
            },
        ),
    ]
