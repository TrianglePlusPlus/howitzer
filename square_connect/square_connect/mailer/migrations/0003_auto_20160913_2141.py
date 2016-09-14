# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0002_person_mailing_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='mailing_list',
            field=models.ForeignKey(to='mailer.MailingList'),
        ),
    ]
