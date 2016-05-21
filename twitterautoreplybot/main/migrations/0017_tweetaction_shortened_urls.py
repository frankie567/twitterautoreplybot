# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetaction',
            name='shortened_urls',
            field=models.TextField(null=True, blank=True),
        ),
    ]
