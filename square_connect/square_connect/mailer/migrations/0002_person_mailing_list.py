# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='mailing_list',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
