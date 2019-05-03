import uuid
from datetime import date

import pytest
from django.core.exceptions import ObjectDoesNotExist

from metarecord.models import Function, Phase, Action, Record
from metarecord.tests.utils import get_bulk_update_function_key


@pytest.mark.django_db
def test_simple_bulk_update_approve(super_user, bulk_update, function, second_function):
    function_1_key = get_bulk_update_function_key(function)
    function_2_key = get_bulk_update_function_key(second_function)
    bulk_update.changes = {
        function_1_key: {
            'attributes': {'TypeSpecifier': 'bulk updated test thing'},
        },
        function_2_key: {
            'attributes': {'TypeSpecifier': 'bulk updated test thing'},
        }
    }
    bulk_update.save(update_fields=['changes'])

    bulk_update.approve(super_user)
    updated_functions = Function.objects.filter(bulk_update=bulk_update)

    assert bulk_update.is_approved
    assert Function.objects.count() == 4  # Old versions should still exist
    assert updated_functions.count() == 2

    for updated_function in updated_functions:
        assert updated_function.attributes == {'TypeSpecifier': 'bulk updated test thing'}


@pytest.mark.django_db
def test_bulk_update_valid_dates(super_user, bulk_update, function):
    function.valid_from = date(2018, 1, 1)
    function.valid_to = date(2019, 1, 1)
    function.save(update_fields=['valid_from', 'valid_to'])

    function_1_key = get_bulk_update_function_key(function)
    bulk_update.changes = {
        function_1_key: {
            'valid_from': '2019-04-01',
            'valid_to': '2019-05-01',
        },
    }
    bulk_update.save(update_fields=['changes'])

    bulk_update.approve(super_user)
    updated_function = Function.objects.filter(bulk_update=bulk_update).first()

    assert bulk_update.is_approved
    assert updated_function.valid_from == date(2019, 4, 1)
    assert updated_function.valid_to == date(2019, 5, 1)


@pytest.mark.django_db
def test_nested_bulk_update_approve(super_user, bulk_update, function, phase, action, record):
    function_key = get_bulk_update_function_key(function)
    attributes = {'TypeSpecifier': 'bulk updated test thing'}
    bulk_update.changes = {
        function_key: {
            'attributes': attributes,
            'phases': {
                phase.uuid.hex: {
                    'attributes': attributes,
                    'actions': {
                        action.uuid.hex: {
                            'attributes': attributes,
                            'records': {
                                record.uuid.hex: {
                                    'attributes': attributes,
                                },
                            },
                        },
                    },
                },
            },
        },
    }
    bulk_update.save(update_fields=['changes'])

    bulk_update.approve(super_user)
    updated_function = Function.objects.get(bulk_update=bulk_update)
    updated_phase = updated_function.phases.first()
    updated_action = updated_phase.actions.first()
    updated_record = updated_action.records.first()

    assert bulk_update.is_approved
    assert updated_function.attributes == attributes
    assert updated_phase.attributes == attributes
    assert updated_action.attributes == attributes
    assert updated_record.attributes == attributes


@pytest.mark.parametrize('location', ('function', 'phase', 'action', 'record'))
@pytest.mark.django_db
def test_invalid_bulk_update_approve(super_user, bulk_update, function, phase, action, record, location):
    function_key = get_bulk_update_function_key(function)
    attributes = {'TypeSpecifier': 'bulk updated test thing'}
    records = {
        record.uuid.hex: {
            'attributes': attributes,
        },
    }
    actions = {
        action.uuid.hex: {
            'attributes': attributes,
            'records': records,
        },
    }
    phases = {
        phase.uuid.hex: {
            'attributes': attributes,
            'actions': actions,
        },
    }
    changes = {
        function_key: {
            'attributes': attributes,
            'phases': phases,
        },
    }

    invalid_uuid = uuid.uuid4().hex

    if location == 'function':
        changes['{}__1'.format(invalid_uuid)] = {'attributes': attributes}
    elif location == 'phase':
        phases[invalid_uuid] = {'attributes': attributes}
    elif location == 'action':
        actions[invalid_uuid] = {'attributes': attributes}
    elif location == 'record':
        records[invalid_uuid] = {'attributes': attributes}

    bulk_update.changes = changes
    bulk_update.save(update_fields=['changes'])

    function_count = Function.objects.count()
    phase_count = Phase.objects.count()
    action_count = Action.objects.count()
    record_count = Record.objects.count()

    exception_type = AttributeError if location == 'function' else ObjectDoesNotExist

    with pytest.raises(exception_type):
        bulk_update.approve(super_user)

    bulk_update.refresh_from_db()

    # Check that nothing has been written to the database
    assert bulk_update.state == Function.DRAFT
    assert not Function.objects.filter(uuid=function.uuid, version__gt=function.version).exists()
    assert Function.objects.count() == function_count
    assert Phase.objects.count() == phase_count
    assert Action.objects.count() == action_count
    assert Record.objects.count() == record_count
