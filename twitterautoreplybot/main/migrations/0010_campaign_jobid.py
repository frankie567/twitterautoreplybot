# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20151119_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='jobId',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
