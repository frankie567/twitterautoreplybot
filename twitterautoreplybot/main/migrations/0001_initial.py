# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet_id', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('query', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='tweet',
            field=models.ForeignKey(to='main.Tweet'),
        ),
    ]
