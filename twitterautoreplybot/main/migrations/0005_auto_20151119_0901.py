# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20151118_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='query',
            field=models.CharField(max_length=255),
        ),
    ]
