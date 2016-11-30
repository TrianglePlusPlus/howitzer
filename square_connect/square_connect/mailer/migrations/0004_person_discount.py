# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0003_auto_20160913_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='discount',
            field=models.CharField(max_length=30, default='all'),
        ),
    ]
