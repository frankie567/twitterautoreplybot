# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20151119_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='running',
            field=models.BooleanField(default=False),
        ),
    ]
