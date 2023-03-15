# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("metarecord", "0032_add_additional_information_and_related_classification"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
BEGIN;
--
-- Alter field attributes on action
--
ALTER TABLE "metarecord_action" ALTER COLUMN "attributes" TYPE jsonb USING "attributes"::jsonb, ALTER COLUMN "attributes" SET DEFAULT '{}';
ALTER TABLE "metarecord_action" ALTER COLUMN "attributes" DROP DEFAULT;
--
-- Alter field attributes on function
--
ALTER TABLE "metarecord_function" ALTER COLUMN "attributes" TYPE jsonb USING "attributes"::jsonb, ALTER COLUMN "attributes" SET DEFAULT '{}';
ALTER TABLE "metarecord_function" ALTER COLUMN "attributes" DROP DEFAULT;
--
-- Alter field attributes on phase
--
ALTER TABLE "metarecord_phase" ALTER COLUMN "attributes" TYPE jsonb USING "attributes"::jsonb, ALTER COLUMN "attributes" SET DEFAULT '{}';
ALTER TABLE "metarecord_phase" ALTER COLUMN "attributes" DROP DEFAULT;
--
-- Alter field attributes on record
--
ALTER TABLE "metarecord_record" ALTER COLUMN "attributes" TYPE jsonb USING "attributes"::jsonb, ALTER COLUMN "attributes" SET DEFAULT '{}';
ALTER TABLE "metarecord_record" ALTER COLUMN "attributes" DROP DEFAULT;
COMMIT;""",
            reverse_sql="""
BEGIN;

CREATE OR REPLACE FUNCTION my_jsonb_to_hstore(jsonb)
  RETURNS hstore
  IMMUTABLE
  STRICT
  LANGUAGE sql
AS $func$
  SELECT COALESCE(hstore(array_agg(key), array_agg(value)), hstore(array[]::varchar[]))
  FROM jsonb_each_text($1)
$func$;

--
-- Alter field attributes on record
--
ALTER TABLE "metarecord_record" ALTER COLUMN "attributes" DROP DEFAULT;
ALTER TABLE "metarecord_record" ALTER COLUMN "attributes" TYPE hstore USING my_jsonb_to_hstore(attributes);
--
-- Alter field attributes on phase
--
ALTER TABLE "metarecord_phase" ALTER COLUMN "attributes" DROP DEFAULT;
ALTER TABLE "metarecord_phase" ALTER COLUMN "attributes" TYPE hstore USING my_jsonb_to_hstore(attributes);
-- 
-- Alter field attributes on function
--
ALTER TABLE "metarecord_function" ALTER COLUMN "attributes" DROP DEFAULT;
ALTER TABLE "metarecord_function" ALTER COLUMN "attributes" TYPE hstore USING my_jsonb_to_hstore(attributes);
--
-- Alter field attributes on action
--
ALTER TABLE "metarecord_action" ALTER COLUMN "attributes" DROP DEFAULT;
ALTER TABLE "metarecord_action" ALTER COLUMN "attributes" TYPE hstore USING my_jsonb_to_hstore(attributes);

DROP FUNCTION my_jsonb_to_hstore(jsonb);

COMMIT;""",
            state_operations=[
                migrations.AlterField(
                    model_name="action",
                    name="attributes",
                    field=django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, default=dict, verbose_name="attributes"
                    ),
                ),
                migrations.AlterField(
                    model_name="function",
                    name="attributes",
                    field=django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, default=dict, verbose_name="attributes"
                    ),
                ),
                migrations.AlterField(
                    model_name="phase",
                    name="attributes",
                    field=django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, default=dict, verbose_name="attributes"
                    ),
                ),
                migrations.AlterField(
                    model_name="record",
                    name="attributes",
                    field=django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, default=dict, verbose_name="attributes"
                    ),
                ),
            ],
        )
    ]
