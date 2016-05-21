# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_campaign_lastrun'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='action',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='query',
        ),
        migrations.AddField(
            model_name='tweetaction',
            name='query',
            field=models.ForeignKey(related_name='tweet_actions', default=None, to='main.Query'),
            preserve_default=False,
        ),
    ]
