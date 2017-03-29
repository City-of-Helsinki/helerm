import pytest
import uuid

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from metarecord.models import Action, Attribute, AttributeGroup, AttributeValue, Function, Phase, Record
from metarecord.tests.utils import set_permissions


@pytest.fixture
def parent_function():
    return Function.objects.create(name='test parent function', function_id='00')


@pytest.fixture
def function(parent_function):
    return Function.objects.create(name='test function', function_id='00 00', parent=parent_function)


@pytest.fixture
def second_function(parent_function):
    return Function.objects.create(name='second test function', function_id='00 01', parent=parent_function)


@pytest.fixture
def phase(function):
    return Phase.objects.create(name='test phase', function=function, index=1)


@pytest.fixture
def action(phase):
    return Action.objects.create(name='test action', phase=phase, index=1)


@pytest.fixture
def record(action):
    return Record.objects.create(name='test record', action=action, index=1)


@pytest.fixture
def choice_attribute():
    return Attribute.objects.create(name='test choice attribute', identifier='ChoiceAttr')


@pytest.fixture
def choice_attribute_2():
    return Attribute.objects.create(name='test choice attribute 2', identifier='ChoiceAttr2')


@pytest.fixture
def free_text_attribute():
    return Attribute.objects.create(name='test free text attribute', identifier='FreeTextAttr')



@pytest.fixture
def free_text_attribute_2():
    return Attribute.objects.create(name='test free text attribute 2', identifier='FreeTextAttr2')


@pytest.fixture
def choice_value_1(choice_attribute):
    return AttributeValue.objects.create(value='test choice value 1', attribute=choice_attribute)


@pytest.fixture
def choice_value_2(choice_attribute):
    return AttributeValue.objects.create(value='test choice value 2', attribute=choice_attribute)


@pytest.fixture
def choice_value_2_1(choice_attribute_2):
    return AttributeValue.objects.create(value='test choice value 2 1', attribute=choice_attribute_2)


@pytest.fixture
def choice_value_2_2(choice_attribute_2):
    return AttributeValue.objects.create(value='test choice value 2 2', attribute=choice_attribute_2)


@pytest.fixture
def template():
    return Function.objects.create(name='test template', is_template=True)


@pytest.fixture
def user():
    return get_user_model().objects.create(
        username='test_user',
        first_name='John',
        last_name='Rambo',
        uuid=uuid.UUID('c2609283-9f53-41e4-8942-014340bb8d52')
    )


@pytest.fixture
def user_2():
    return get_user_model().objects.create(
        username='test_user_2',
        first_name='Rocky',
        last_name='Balboa',
        uuid=uuid.UUID('7c248eb0-263f-4321-ba46-474a48f5e208')
    )


@pytest.fixture
def super_user():
    return get_user_model().objects.create(
        username='test_super_user',
        first_name='Kurt',
        last_name='Sloane',
        uuid=uuid.UUID('e96d474b-6eee-45af-94f8-7d48292036f4')
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_api_client(user):
    api_client = APIClient()
    api_client.force_authenticate(user)
    api_client.user = user
    return api_client


@pytest.fixture
def user_2_api_client(user_2):
    api_client = APIClient()
    api_client.force_authenticate(user_2)
    api_client.user = user_2
    return api_client


@pytest.fixture
def super_user_api_client(super_user):
    api_client = APIClient()
    api_client.force_authenticate(super_user)
    api_client.user = super_user
    set_permissions(api_client, (Function.CAN_EDIT, Function.CAN_REVIEW, Function.CAN_APPROVE))
    return api_client


@pytest.fixture
def attribute_group(choice_attribute):
    group = AttributeGroup.objects.create(name='test attribute group')
    choice_attribute.group = group
    choice_attribute.save(update_fields=('group',))
    return group
