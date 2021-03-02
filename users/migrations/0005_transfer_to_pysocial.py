from django.db import connection, migrations
from django.db.utils import IntegrityError


def transfer_users_from_allauth_to_pysocial(apps, schema_editor):
    """
    Transfer user UIDs from Allauth to Python Social Auth.
    Has to be done in raw SQL since Django does not recognize allauth after removing it from the project.
    """
    all_tables = connection.introspection.table_names()
    if "socialaccount_socialaccount" in all_tables:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO social_auth_usersocialauth (user_id, provider, uid, extra_data, created, modified)"
                    "SELECT user_id, 'tunnistamo', uid, extra_data, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP FROM socialaccount_socialaccount;"
                )
        except IntegrityError:
            connection._rollback()


def remove_sessions(apps, schema_editor):
    """
    This needs to be done to get rid of the old sessions because of the
    added setting SESSION_SERIALIZER.
    """
    Session = apps.get_model("sessions", "Session")
    Session.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_longer_first_name"),
    ]

    operations = [
        migrations.RunPython(
            transfer_users_from_allauth_to_pysocial, migrations.RunPython.noop,
        ),
        migrations.RunPython(remove_sessions, migrations.RunPython.noop,),
    ]
