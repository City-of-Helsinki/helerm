from django.db import migrations


def fix_bulk_update_permissions(apps, schema_editor):
    """
    Replace usage of incorrect permission object that might exist in the database
    with the correct permission object and delete the incorrect object if it exists.
    """
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    User = apps.get_model('users', 'User')

    correct_perm = Permission.objects.get(codename='approve_bulkupdate')
    wrong_perm = Permission.objects.filter(codename='metarecord.approve_bulkupdate').first()

    if wrong_perm:
        for group in Group.objects.filter(permissions__in=[wrong_perm]):
            group.permissions.add(correct_perm)
            group.permissions.remove(wrong_perm)

        for user in User.objects.filter(user_permissions__in=[wrong_perm]):
            user.user_permissions.add(correct_perm)
            user.user_permissions.remove(wrong_perm)

        wrong_perm.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('metarecord', '0043_add_name_and_help_text_to_attribute_value'),
    ]

    operations = [
        migrations.RunPython(fix_bulk_update_permissions, migrations.RunPython.noop),
    ]
