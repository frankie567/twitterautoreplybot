# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_campaign_jobid'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='answerWithImage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='query',
            name='requiredNumberOfImages',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
