# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-06 13:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.contrib.postgres.fields import HStoreField
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('metarecord', '0013_add_function_is_template'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Action',
        ),
        migrations.DeleteModel(
            name='Function',
        ),
        migrations.DeleteModel(
            name='Phase',
        ),
        migrations.DeleteModel(
            name='Record',
        ),
        migrations.DeleteModel(
            name='RecordType',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='AttributeValue',
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of creation')),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of modification')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('index', models.PositiveSmallIntegerField(db_index=True, editable=False, null=True)),
                ('attributes', HStoreField(blank=True, null=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='action_created', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='action_modified', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
            ],
            options={
                'ordering': ('phase', 'index'),
                'verbose_name': 'action',
                'verbose_name_plural': 'actions',
            },
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of creation')),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of modification')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('identifier', models.CharField(db_index=True, max_length=64, unique=True, verbose_name='identifier')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
            ],
            options={
                'verbose_name': 'attribute',
                'verbose_name_plural': 'attributes',
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of creation')),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of modification')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=1024, verbose_name='value')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='metarecord.Attribute', verbose_name='attribute')),
            ],
            options={
                'verbose_name': 'attribute value',
                'verbose_name_plural': 'attribute values',
            },
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of creation')),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of modification')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('index', models.PositiveSmallIntegerField(db_index=True, editable=False, null=True)),
                ('attributes', HStoreField(blank=True, null=True)),
                ('function_id', models.CharField(db_index=True, max_length=16, null=True, unique=True, verbose_name='function ID')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('error_count', models.PositiveIntegerField(default=0)),
                ('is_template', models.BooleanField(default=False, verbose_name='is template')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='function_created', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='function_modified', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='metarecord.Function', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'function',
                'verbose_name_plural': 'functions',
            },
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of creation')),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of modification')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('index', models.PositiveSmallIntegerField(db_index=True, editable=False, null=True)),
                ('attributes', HStoreField(blank=True, null=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phase_created', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phases', to='metarecord.Function', verbose_name='function')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phase_modified', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
            ],
            options={
                'ordering': ('function', 'index'),
                'verbose_name': 'phase',
                'verbose_name_plural': 'phases',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of creation')),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of modification')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('index', models.PositiveSmallIntegerField(db_index=True, editable=False, null=True)),
                ('attributes', HStoreField(blank=True, null=True)),
                ('name', models.CharField(max_length=256, verbose_name='type specifier')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='metarecord.Action', verbose_name='action')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='record_created', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='record_modified', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='metarecord.Record', verbose_name='parent')),
            ],
            options={
                'ordering': ('action', 'index'),
                'verbose_name': 'record',
                'verbose_name_plural': 'records',
            },
        ),
        migrations.CreateModel(
            name='RecordType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of creation')),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='time of modification')),
                ('value', models.CharField(max_length=256, verbose_name='name')),
            ],
            options={
                'verbose_name': 'record type',
                'verbose_name_plural': 'record types',
            },
        ),
        migrations.AddField(
            model_name='record',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='metarecord.RecordType', verbose_name='type'),
        ),
        migrations.AddField(
            model_name='action',
            name='phase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='metarecord.Phase', verbose_name='phase'),
        ),
        migrations.AlterUniqueTogether(
            name='attributevalue',
            unique_together=set([('attribute', 'value')]),
        ),
    ]
