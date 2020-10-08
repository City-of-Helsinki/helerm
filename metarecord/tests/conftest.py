import uuid

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from metarecord.models import Action, Attribute, AttributeGroup, AttributeValue, Classification, Function, Phase, Record
from metarecord.models.bulk_update import BulkUpdate
from metarecord.tests.utils import set_permissions


@pytest.fixture
def parent_classification():
    return Classification.objects.create(title='test parent classification', code='00', function_allowed=False)


@pytest.fixture
def classification():
    return Classification.objects.create(
        title='test classification',
        code='00 00',
        state=Classification.APPROVED,
        function_allowed=True,
    )


@pytest.fixture
def classification_2():
    return Classification.objects.create(
        title='test classification 2',
        code='00 01',
        state=Classification.APPROVED,
        function_allowed=True
    )


@pytest.fixture
def function(classification):
    return Function.objects.create(classification=classification)


@pytest.fixture
def second_function(classification_2):
    return Function.objects.create(classification=classification_2)


@pytest.fixture
def phase(function):
    return Phase.objects.create(attributes={'TypeSpecifier': 'test phase'}, function=function, index=1)


@pytest.fixture
def action(phase):
    return Action.objects.create(attributes={'TypeSpecifier': 'test action'}, phase=phase, index=1)


@pytest.fixture
def record(action):
    return Record.objects.create(attributes={'TypeSpecifier': 'test record'}, action=action, index=1)


@pytest.fixture
def bulk_update():
    return BulkUpdate.objects.create(
        description='Lorem ipsum dolor sit amet',
        state=Function.DRAFT,
        changes={}
    )


@pytest.fixture
def choice_attribute():
    return Attribute.objects.create(
        name='test choice attribute', identifier='ChoiceAttr', help_text='test choice attribute help text'
    )


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
    return AttributeValue.objects.create(
        value='test choice value 1', attribute=choice_attribute, name="test name", help_text="test help_text"
    )


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
    return Function.objects.create(is_template=True)


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
        is_superuser=True,
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
    set_permissions(api_client, (Function.CAN_EDIT, Function.CAN_REVIEW, Function.CAN_APPROVE,
                                 Function.CAN_VIEW_MODIFIED_BY, 'metarecord.delete_function'))
    return api_client


@pytest.fixture
def attribute_group(choice_attribute):
    group = AttributeGroup.objects.create(name='test attribute group')
    choice_attribute.group = group
    choice_attribute.save(update_fields=('group',))
    return group
