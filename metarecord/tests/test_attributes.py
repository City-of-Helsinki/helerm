import pytest

from metarecord.models import Attribute


def _assert_attribute_value(function, attribute, value):
    value_obj = function.attribute_values.get(attribute__identifier=attribute)
    assert value_obj.value == value


@pytest.mark.django_db
def test_get_choice_attribute_value(function, choice_attribute, second_function, choice_value_1):
    second_function.attribute_values.add(choice_value_1)  # this should not affect anything
    assert function.get_attribute_value('ChoiceAttr') is None

    function.attribute_values.add(choice_value_1)
    assert function.get_attribute_value('ChoiceAttr') == 'test choice value 1'

    with pytest.raises(Attribute.DoesNotExist):
        function.get_attribute_value('NonExistingAttr')


@pytest.mark.django_db
def test_get_free_text_attribute_value(function, second_function, free_text_attribute, free_text_value_1):
    second_function.attribute_values.add(free_text_value_1)  # this should not affect anything
    assert function.get_attribute_value('FreeTextAttr') is None

    second_function.attribute_values.remove(free_text_value_1)
    function.attribute_values.add(free_text_value_1)
    assert function.get_attribute_value('FreeTextAttr') == 'test free text value 1'


@pytest.mark.django_db
def test_set_choice_attribute_value(function, second_function, choice_attribute, choice_value_1, choice_value_2):
    function.set_attribute_value('ChoiceAttr', 'test choice value 1')
    second_function.set_attribute_value('ChoiceAttr', 'test choice value 1')

    _assert_attribute_value(function, 'ChoiceAttr', 'test choice value 1')
    _assert_attribute_value(second_function, 'ChoiceAttr', 'test choice value 1')
    assert choice_attribute.values.count() == 2

    function.set_attribute_value('ChoiceAttr', 'test choice value 2')
    _assert_attribute_value(function, 'ChoiceAttr', 'test choice value 2')
    _assert_attribute_value(second_function, 'ChoiceAttr', 'test choice value 1')
    assert choice_attribute.values.count() == 2

    # set the same value again
    function.set_attribute_value('ChoiceAttr', 'test choice value 2')
    _assert_attribute_value(function, 'ChoiceAttr', 'test choice value 2')
    assert choice_attribute.values.count() == 2


@pytest.mark.django_db
def test_set_free_text_attribute_value(function, second_function, free_text_attribute):

    # set first function's free text attribute
    function.set_attribute_value('FreeTextAttr', 'some text')
    _assert_attribute_value(function, 'FreeTextAttr', 'some text')
    assert free_text_attribute.values.count() == 1

    # set the same text for the other function
    second_function.set_attribute_value('FreeTextAttr', 'some text')
    _assert_attribute_value(second_function, 'FreeTextAttr', 'some text')
    assert free_text_attribute.values.count() == 2  # both functions should have their own values with the same text

    # change first function's attribute value
    function.set_attribute_value('FreeTextAttr', 'some text that has changed')
    _assert_attribute_value(function, 'FreeTextAttr', 'some text that has changed')

    # check that the other value hasn't changed
    _assert_attribute_value(second_function, 'FreeTextAttr', 'some text')
    assert free_text_attribute.values.count() == 2

    # set the same value again
    function.set_attribute_value('FreeTextAttr', 'some text that has changed')
    _assert_attribute_value(function, 'FreeTextAttr', 'some text that has changed')
    assert free_text_attribute.values.count() == 2


@pytest.mark.django_db
def test_remove_choice_attribute_value(function, second_function, choice_attribute, choice_value_1, choice_value_2):
    function.attribute_values.add(choice_value_1)
    second_function.attribute_values.add(choice_value_1)

    function.remove_attribute_value('ChoiceAttr')
    assert function.attribute_values.all().count() == 0
    assert second_function.attribute_values.all().count() == 1
    assert choice_attribute.values.count() == 2

    # remove non existing value
    function.remove_attribute_value('ChoiceAttr')


@pytest.mark.django_db
def test_remove_free_text_attribute_value(function, second_function, free_text_attribute, free_text_value_1,
                                          free_text_value_2):
    function.attribute_values.add(free_text_value_1)
    second_function.attribute_values.add(free_text_value_2)

    function.remove_attribute_value('FreeTextAttr')
    assert function.attribute_values.all().count() == 0
    assert second_function.attribute_values.all().count() == 1
    assert free_text_attribute.values.count() == 1  # one value should have been deleted

    # remove non existing value
    function.remove_attribute_value('FreeTextAttr')
    assert free_text_attribute.values.count() == 1

# TODO test free text attributes with StructuralElement object and bulk delete
