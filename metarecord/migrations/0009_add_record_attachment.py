# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 21:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("metarecord", "0008_longer_attribute_values"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecordAttachment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="time of creation",
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="time of modification",
                    ),
                ),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        db_index=True, editable=False, null=True
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=256, verbose_name="type specifier"),
                ),
                (
                    "attribute_values",
                    models.ManyToManyField(
                        to="metarecord.AttributeValue", verbose_name="attribute values"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recordattachment_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recordattachment_modified",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="modified by",
                    ),
                ),
                (
                    "record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="metarecord.Record",
                        verbose_name="record",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "record attachments",
                "verbose_name": "record attachment",
            },
        ),
    ]
