# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('answerSentence', models.TextField()),
                ('running', models.BooleanField(default=False)),
                ('lastRun', models.DateTimeField(null=True, editable=False, blank=True)),
                ('jobId', models.CharField(max_length=255, null=True, editable=False, blank=True)),
                ('creator', models.ForeignKey(related_name='campaigns', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.CharField(max_length=255)),
                ('correspondingSentence', models.CharField(max_length=255)),
                ('requiredNumberOfImages', models.IntegerField(null=True, blank=True)),
                ('answerWithImage', models.BooleanField(default=False)),
                ('campaign', models.ForeignKey(related_name='queries', to='main.Campaign')),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TweetAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shortened_urls', models.TextField(null=True, blank=True)),
                ('clicked', models.BooleanField(default=False)),
                ('prefrCreated', models.BooleanField(default=False)),
                ('action', models.ForeignKey(to='main.Action')),
                ('campaign', models.ForeignKey(related_name='tweet_actions', to='main.Campaign')),
                ('query', models.ForeignKey(related_name='tweet_actions', to='main.Query')),
                ('tweet', models.ForeignKey(related_name='tweet_actions', to='main.Tweet')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='tweet',
            field=models.ForeignKey(related_name='images', to='main.Tweet'),
        ),
    ]
