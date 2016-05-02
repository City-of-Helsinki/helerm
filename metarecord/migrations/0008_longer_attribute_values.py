# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 20:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metarecord', '0007_attribute_is_free_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recordtype',
            options={'verbose_name': 'record type', 'verbose_name_plural': 'record types'},
        ),
        migrations.AlterField(
            model_name='attributevalue',
            name='value',
            field=models.CharField(max_length=1024, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='record',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='metarecord.RecordType', verbose_name='type'),
        ),
    ]