import pytest
from django.core.management import call_command

from metarecord.models import Function, Phase, Action, Record
from metarecord.models.bulk_update import BulkUpdate


def _prepare_structural_element(obj, cls, user, user_2):
    obj.created_by = user
    obj.modified_by = user_2
    obj.save(update_fields=['created_by', 'modified_by'])
    cls.objects.filter(pk=obj.pk).update(_created_by='', _modified_by='')


@pytest.mark.django_db
def test_function_migration(function, user, user_2):
    _prepare_structural_element(function, Function, user, user_2)
    function.refresh_from_db()
    assert function._created_by == ''
    assert function._modified_by == ''

    call_command('migrate', app_label='metarecord', migration_name='0044', skip_checks=True, fake=True)
    call_command('migrate', app_label='metarecord', migration_name='0045', skip_checks=True)

    function.refresh_from_db()
    assert function._created_by == 'John Rambo'
    assert function._modified_by == 'Rocky Balboa'


@pytest.mark.django_db
def test_phase_migration(phase, user, user_2):
    _prepare_structural_element(phase, Phase, user, user_2)
    phase.refresh_from_db()
    assert phase._created_by == ''
    assert phase._modified_by == ''

    call_command('migrate', app_label='metarecord', migration_name='0044', skip_checks=True, fake=True)
    call_command('migrate', app_label='metarecord', migration_name='0045', skip_checks=True)

    phase.refresh_from_db()
    assert phase._created_by == 'John Rambo'
    assert phase._modified_by == 'Rocky Balboa'


@pytest.mark.django_db
def test_action_migration(action, user, user_2):
    _prepare_structural_element(action, Action, user, user_2)
    action.refresh_from_db()
    assert action._created_by == ''
    assert action._modified_by == ''

    call_command('migrate', app_label='metarecord', migration_name='0044', skip_checks=True, fake=True)
    call_command('migrate', app_label='metarecord', migration_name='0045', skip_checks=True)

    action.refresh_from_db()
    assert action._created_by == 'John Rambo'
    assert action._modified_by == 'Rocky Balboa'


@pytest.mark.django_db
def test_record_migration(record, user, user_2):
    _prepare_structural_element(record, Record, user, user_2)
    record.refresh_from_db()
    assert record._created_by == ''
    assert record._modified_by == ''

    call_command('migrate', app_label='metarecord', migration_name='0044', skip_checks=True, fake=True)
    call_command('migrate', app_label='metarecord', migration_name='0045', skip_checks=True)

    record.refresh_from_db()
    assert record._created_by == 'John Rambo'
    assert record._modified_by == 'Rocky Balboa'


@pytest.mark.django_db
def test_bulk_update_migration(bulk_update, user, user_2, super_user):
    BulkUpdate.objects.filter(pk=bulk_update.pk).update(
        approved_by=super_user,
        created_by=user,
        modified_by=user_2,
    )
    bulk_update.refresh_from_db()
    assert bulk_update._approved_by == ''
    assert bulk_update._created_by == ''
    assert bulk_update._modified_by == ''

    call_command('migrate', app_label='metarecord', migration_name='0044', skip_checks=True, fake=True)
    call_command('migrate', app_label='metarecord', migration_name='0045', skip_checks=True)

    bulk_update.refresh_from_db()
    assert bulk_update._approved_by == 'Kurt Sloane'
    assert bulk_update._created_by == 'John Rambo'
    assert bulk_update._modified_by == 'Rocky Balboa'


@pytest.mark.django_db
def test_metadata_version_migration(function, user):
    _prepare_structural_element(function, Function, user, user)
    function.refresh_from_db()
    function.create_metadata_version()
    function.metadata_versions.update(_modified_by='')
    metadata_version = function.metadata_versions.first()
    assert metadata_version._modified_by == ''

    call_command('migrate', app_label='metarecord', migration_name='0044', skip_checks=True, fake=True)
    call_command('migrate', app_label='metarecord', migration_name='0045', skip_checks=True)

    metadata_version.refresh_from_db()
    assert metadata_version._modified_by == 'John Rambo'


@pytest.mark.django_db
def test_migration_without_user(function):
    assert function.created_by == None
    assert function._created_by == ''

    call_command('migrate', app_label='metarecord', migration_name='0044', skip_checks=True, fake=True)
    call_command('migrate', app_label='metarecord', migration_name='0045', skip_checks=True)

    function.refresh_from_db()
    assert function._created_by == ''


@pytest.mark.django_db
def test_migration_without_first_name(function, user, user_2):
    user.first_name = ''
    user.save(update_fields=['first_name'])
    _prepare_structural_element(function, Function, user, user_2)
    function.refresh_from_db()
    assert function._created_by == ''
    assert function.created_by.get_full_name() == 'Rambo'

    call_command('migrate', app_label='metarecord', migration_name='0044', skip_checks=True, fake=True)
    call_command('migrate', app_label='metarecord', migration_name='0045', skip_checks=True)

    function.refresh_from_db()
    assert function._created_by == 'Rambo'


@pytest.mark.django_db
def test_migration_without_last_name(function, user, user_2):
    user.last_name = ''
    user.save(update_fields=['last_name'])
    _prepare_structural_element(function, Function, user, user_2)
    function.refresh_from_db()
    assert function._created_by == ''
    assert function.created_by.get_full_name() == 'John'

    call_command('migrate', app_label='metarecord', migration_name='0044', skip_checks=True, fake=True)
    call_command('migrate', app_label='metarecord', migration_name='0045', skip_checks=True)

    function.refresh_from_db()
    assert function._created_by == 'John'


@pytest.mark.django_db
def test_migration_wouthout_names(function, user, user_2):
    user.first_name = ''
    user.last_name = ''
    user.save(update_fields=['first_name', 'last_name'])
    _prepare_structural_element(function, Function, user, user_2)
    function.refresh_from_db()
    assert function._created_by == ''
    assert function.created_by.get_full_name() == ''

    call_command('migrate', app_label='metarecord', migration_name='0044', skip_checks=True, fake=True)
    call_command('migrate', app_label='metarecord', migration_name='0045', skip_checks=True)

    function.refresh_from_db()
    assert function._created_by == ''
