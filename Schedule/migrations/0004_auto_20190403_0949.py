# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-03 09:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0003_auto_20190403_0839'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='completed',
            new_name='notified',
        ),
    ]
