# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 03:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20170414_0345'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='book',
            index_together=set([('id', 'slug')]),
        ),
    ]
