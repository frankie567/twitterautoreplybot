# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.TextField()),
                ('correspondingSentence', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='tweet',
            name='action',
            field=models.ForeignKey(to='main.Action'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='query',
            field=models.ForeignKey(to='main.Query'),
        ),
    ]
