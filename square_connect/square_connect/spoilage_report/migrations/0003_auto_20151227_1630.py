# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 22:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spoilage_report', '0002_spoilageitem_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spoilageitem',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='spoilageitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='spoilageitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='spoilageitem',
            name='sku',
            field=models.CharField(default='', max_length=12),
        ),
    ]
