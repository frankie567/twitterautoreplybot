# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20151119_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='jobId',
            field=models.CharField(max_length=255, null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='lastRun',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
    ]
