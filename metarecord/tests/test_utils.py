import pytest

from metarecord.utils import (
    create_new_function_version,
    model_to_dict,
    update_nested_dictionary,
)


def test_simple_dict_update():
    dict1 = {
        'a': '123',
        'b': '321',
    }
    dict2 = {
        'a': '1234',
        'c': 'asd',
    }

    updated = update_nested_dictionary(dict1, dict2)

    assert updated == {
        'a': '1234',
        'b': '321',
        'c': 'asd',
    }


def test_dict_in_dict_update():
    dict1 = {
        'a': {
            'b': '123',
            'c': '321',
        },
    }
    dict2 = {
        'a': {
            'b': '1234',
            'd': 'asd',
        },
    }

    updated = update_nested_dictionary(dict1, dict2)

    assert updated == {
        'a': {
            'b': '1234',
            'c': '321',
            'd': 'asd',
        },
    }


def test_dict_to_str_update():
    dict1 = {
        'a': {
            'b': '123',
            'c': '321',
        },
        'd': 'qwerty',
    }
    dict2 = {
        'a': '123 321',
    }

    updated = update_nested_dictionary(dict1, dict2)

    assert updated == {
        'a': '123 321',
        'd': 'qwerty',
    }


def test_nested_dict_update():
    dict1 = {
        'a': {
            'b': '123',
            'c': [1, 2, 3],
            'd': {
                'e': True,
                'f': [4, 5],
            },
        },
    }
    dict2 = {
        'a': {
            'c': [1, 2],
            'd': {
                'f': [3, 4, 5],
                'g': '456',
            },
        },
    }

    updated = update_nested_dictionary(dict1, dict2)

    assert updated == {
        'a': {
            'b': '123',
            'c': [1, 2],
            'd': {
                'e': True,
                'f': [3, 4, 5],
                'g': '456',
            },
        },
    }


@pytest.mark.django_db
def test_model_to_dict(function):
    d = model_to_dict(function)

    assert d['id'] == function.id
    assert d['uuid'] == function.uuid
    assert d['classification'] == function.classification


@pytest.mark.django_db
def test_model_to_dict_fields(function):
    d = model_to_dict(function, fields=('id', 'uuid'))

    assert len(d) == 2
    assert 'id' in d.keys()
    assert 'uuid' in d.keys()


@pytest.mark.django_db
def test_model_to_dict_exclude(function):
    d = model_to_dict(function, exclude=('id', 'uuid'))

    assert d  # The result isn't empty
    assert 'id' not in d.keys()
    assert 'uuid' not in d.keys()


@pytest.mark.django_db
def test_create_new_function_version(super_user, function, phase, action, record):
    new_function = create_new_function_version(function, super_user)
    new_phase = new_function.phases.first()
    new_action = new_phase.actions.first()
    new_record = new_action.records.first()

    assert new_function.uuid == function.uuid
    assert new_function.version == function.version + 1
    assert new_function.classification == function.classification
    assert new_function.name == function.name
    assert new_function.attributes == function.attributes
    assert new_function.modified_by == super_user

    assert new_phase.uuid == phase.uuid
    assert new_phase.attributes == phase.attributes
    assert new_phase.modified_by == super_user

    assert new_action.uuid == action.uuid
    assert new_action.attributes == action.attributes
    assert new_action.modified_by == super_user

    assert new_record.uuid == record.uuid
    assert new_record.attributes == record.attributes
    assert new_record.modified_by == super_user
