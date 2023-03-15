# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-21 13:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("metarecord", "0023_add_attribute_value_index"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="attributevalue",
            unique_together=set([("attribute", "index"), ("attribute", "value")]),
        ),
    ]
