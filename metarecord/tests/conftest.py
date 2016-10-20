import pytest

from metarecord.models import Action, Attribute, AttributeValue, Function, Phase, Record, RecordType


@pytest.fixture
def function():
    return Function.objects.create(name='test function', function_id='00 00')


@pytest.fixture
def second_function():
    return Function.objects.create(name='second test function', function_id='00 01')


@pytest.fixture
def phase(function):
    return Phase.objects.create(name='test phase', function=function)


@pytest.fixture
def action(phase):
    return Action.objects.create(name='test action', phase=phase)


@pytest.fixture
def record_type():
    return RecordType.objects.create(value='test record type')


@pytest.fixture
def record(action, record_type):
    return Record.objects.create(name='test record', action=action, type=record_type)


@pytest.fixture
def choice_attribute():
    return Attribute.objects.create(name='test choice attribute', identifier='ChoiceAttr')


@pytest.fixture
def free_text_attribute():
    return Attribute.objects.create(name='test free text attribute', identifier='FreeTextAttr', is_free_text=True)


@pytest.fixture
def choice_value_1(choice_attribute):
    return AttributeValue.objects.create(value='test choice value 1', attribute=choice_attribute)


@pytest.fixture
def choice_value_2(choice_attribute):
    return AttributeValue.objects.create(value='test choice value 2', attribute=choice_attribute)


@pytest.fixture
def free_text_value_1(free_text_attribute):
    return AttributeValue.objects.create(value='test free text value 1', attribute=free_text_attribute)


@pytest.fixture
def free_text_value_2(free_text_attribute):
    return AttributeValue.objects.create(value='test free text value 2', attribute=free_text_attribute)
