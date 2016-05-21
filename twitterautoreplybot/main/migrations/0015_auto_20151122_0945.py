# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20151122_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='creator',
            field=models.ForeignKey(related_name='campaigns', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
