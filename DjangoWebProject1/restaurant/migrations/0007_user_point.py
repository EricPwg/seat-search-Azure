# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_auto_20170624_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='point',
            field=models.DecimalField(decimal_places=0, default=100, max_digits=10),
        ),
    ]