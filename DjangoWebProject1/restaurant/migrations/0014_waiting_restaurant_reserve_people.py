# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0013_auto_20170629_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='waiting',
            name='restaurant_reserve_people',
            field=models.DecimalField(decimal_places=0, default=4, max_digits=2),
        ),
    ]
