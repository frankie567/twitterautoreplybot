# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_campaign_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='creator',
            field=models.ForeignKey(related_name='campaigns', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
