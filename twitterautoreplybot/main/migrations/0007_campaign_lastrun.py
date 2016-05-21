# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_campaign_running'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='lastRun',
            field=models.DateTimeField(null=True),
        ),
    ]
