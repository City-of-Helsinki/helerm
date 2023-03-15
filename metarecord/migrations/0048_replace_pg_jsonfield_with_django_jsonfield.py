# Generated by Django 3.1.5 on 2021-01-11 09:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metarecord", "0047_approve_existing_classifications"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="attributes",
            field=models.JSONField(blank=True, default=dict, verbose_name="attributes"),
        ),
        migrations.AlterField(
            model_name="bulkupdate",
            name="changes",
            field=models.JSONField(blank=True, default=dict, verbose_name="changes"),
        ),
        migrations.AlterField(
            model_name="function",
            name="attributes",
            field=models.JSONField(blank=True, default=dict, verbose_name="attributes"),
        ),
        migrations.AlterField(
            model_name="phase",
            name="attributes",
            field=models.JSONField(blank=True, default=dict, verbose_name="attributes"),
        ),
        migrations.AlterField(
            model_name="record",
            name="attributes",
            field=models.JSONField(blank=True, default=dict, verbose_name="attributes"),
        ),
    ]
