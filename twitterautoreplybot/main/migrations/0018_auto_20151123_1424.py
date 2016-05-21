# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_tweetaction_shortened_urls'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetaction',
            name='clicked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tweetaction',
            name='prefrCreated',
            field=models.BooleanField(default=False),
        ),
    ]
