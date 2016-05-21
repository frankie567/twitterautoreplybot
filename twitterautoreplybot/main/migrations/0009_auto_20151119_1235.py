# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20151119_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='lastRun',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
