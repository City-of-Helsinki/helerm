from metarecord.utils import update_nested_dictionary


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
