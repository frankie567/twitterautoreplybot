# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20151117_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('answerSentence', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TweetAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.ForeignKey(to='main.Action')),
                ('campaign', models.ForeignKey(related_name='tweet_actions', to='main.Campaign')),
                ('tweet', models.ForeignKey(related_name='tweet_actions', to='main.Tweet')),
            ],
        ),
        migrations.AddField(
            model_name='query',
            name='campaign',
            field=models.ForeignKey(related_name='queries', default=None, to='main.Campaign'),
            preserve_default=False,
        ),
    ]
