# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20151117_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='tweet',
            field=models.ForeignKey(related_name='images', to='main.Tweet'),
        ),
    ]
