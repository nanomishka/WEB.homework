# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0002_auto_20141221_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quest_tags',
            name='t_tag',
        ),
        migrations.DeleteModel(
            name='Quest_tags',
        ),
        migrations.AddField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tags',
            name='questions',
            field=models.ManyToManyField(to='ask.Question'),
            preserve_default=True,
        ),
    ]
