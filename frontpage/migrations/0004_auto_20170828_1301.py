# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-28 04:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0003_summer_note_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summer_note_model',
            name='attachment_ptr',
        ),
        migrations.DeleteModel(
            name='summer_note_model',
        ),
    ]