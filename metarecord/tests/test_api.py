import pytest
from rest_framework.reverse import reverse
from metarecord.models import Function


FUNCTION_LIST_URL = reverse('v1:function-list')


def get_function_detail_url(function):
    return reverse('v1:function-detail', kwargs={'uuid': function.uuid})


@pytest.fixture
def function_data(parent_function, function, free_text_attribute, choice_attribute):
    return {
        'name': 'new function',
        'function_id': function.function_id,
        'parent': parent_function.uuid,
        'attributes': {
            free_text_attribute.identifier: 'new function attribute value',
        },
        'phases': [
            {
                'name': 'new phase',
                'actions': [
                    {
                        'name': 'new action',
                        'records': [
                            {
                                'name': 'new record',
                                'attributes': {
                                    choice_attribute.identifier: 'new record attribute value',
                                },
                            }
                        ]
                    }
                ]
            }
        ]
    }


def _check_function_object_matches_data(function_obj, data):
    new_function = function_obj

    assert new_function.parent == Function.objects.latest_version().get(uuid=data['parent'])
    assert new_function.name == data['name']
    assert new_function.attributes == data['attributes']
    assert new_function.phases.count() == 1

    new_phase = new_function.phases.first()
    phase_data = data['phases'][0]
    assert new_phase.name == phase_data['name']
    assert new_phase.attributes == {}
    assert new_phase.actions.count() == 1

    new_action = new_phase.actions.first()
    action_data = phase_data['actions'][0]
    assert new_action.name == action_data['name']
    assert new_action.attributes == {}
    assert new_action.records.count() == 1

    new_record = new_action.records.first()
    record_data = action_data['records'][0]
    assert new_record.name == record_data['name']
    assert new_record.attributes == record_data['attributes']


@pytest.fixture
def attribute(choice_attribute):
    return choice_attribute


@pytest.mark.parametrize('resource', [
    'function',
    'phase',
    'action',
    'record',
    'attribute',
    'template',
])
@pytest.mark.django_db
def test_get(api_client, resource, function, phase, action, record, attribute, template):
    """
    Test GET to every resource's list and detail endpoint.
    """
    list_url = reverse('v1:%s-list' % resource)
    response = api_client.get(list_url)
    assert response.status_code == 200
    assert len(response.data['results'])

    id_field = 'pk' if resource is 'attribute' else 'uuid'
    id_value = getattr(locals().get(resource), id_field)
    detail_url = reverse('v1:%s-detail' % resource.replace('_', ''), kwargs={id_field: id_value})
    response = api_client.get(detail_url)
    assert response.status_code == 200
    assert response.data


@pytest.mark.django_db
def test_get_attribute_schemas(api_client):
    url = '{}schemas/'.format(reverse('v1:attribute-list'))
    response = api_client.get(url)
    assert response.status_code == 200

    for element in ('function', 'phase', 'action', 'record'):
        assert len(response.data.get(element))


@pytest.mark.django_db
def test_function_versioning(api_client):
    first_draft = Function.objects.create(name='first draft', function_id='00 00')
    first_approved = Function.objects.create(name='first approved', function_id='00 00', state=Function.APPROVED)
    second_approved = Function.objects.create(name='second approved', function_id='00 00', state=Function.APPROVED)
    second_draft = Function.objects.create(name='second draft', function_id='00 00')
    other_function = Function.objects.create(name='other function', function_id='00 01')
    template = Function.objects.create(name='template', is_template=True)

    assert first_draft.uuid == first_approved.uuid == second_approved.uuid == second_draft.uuid
    assert first_draft.version == 1
    assert first_approved.version == 2
    assert second_approved.version == 3
    assert second_draft.version == 4
    assert other_function.version == 1
    assert template.version is None

    url = reverse('v1:function-detail', kwargs={'uuid': first_draft.uuid})

    # /function/<uuid>/ should return the latest version
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == 'second draft'

    # /function/<uuid>/?state=approved should return the latest approved version
    response = api_client.get(url + '?state=approved')
    assert response.status_code == 200
    assert response.data['name'] == 'second approved'


@pytest.mark.django_db
def test_unauthenticated_user_cannot_post_or_put_functions(function_data, api_client, function):
    response = api_client.post(FUNCTION_LIST_URL, data=function_data)
    assert response.status_code == 401

    response = api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_cannot_patch_or_delete_functions(function_data, user_api_client, function):
    response = user_api_client.patch(get_function_detail_url(function), data=function_data)
    assert response.status_code == 405

    response = user_api_client.delete(get_function_detail_url(function))
    assert response.status_code == 405


@pytest.mark.django_db
def test_function_post(function_data, user_api_client):
    function_data['function_id'] = '00 77'
    response = user_api_client.post(FUNCTION_LIST_URL, data=function_data)
    assert response.status_code == 201

    new_function = Function.objects.last()
    _check_function_object_matches_data(new_function, function_data)

    assert new_function.version == 1
    assert new_function.state == Function.DRAFT


@pytest.mark.django_db
def test_function_put(function_data, user_api_client, function, phase, action, record):
    models = (function, phase, action, record)
    modified_ats = [obj.modified_at for obj in models]  # store original modified_at timestamps

    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 200

    new_function = Function.objects.last()
    _check_function_object_matches_data(new_function, function_data)

    assert new_function.version == 2
    assert new_function.uuid == function.uuid

    # check that the original objects haven't been modified
    for index, obj in enumerate(models):
        obj.refresh_from_db()
        assert obj.modified_at == modified_ats[index]


@pytest.mark.django_db
def test_function_post_function_id_exists_already(function_data, user_api_client, function):
    function_data['function_id'] = function.function_id

    response = user_api_client.post(FUNCTION_LIST_URL, data=function_data)
    assert response.status_code == 400
    assert response.data['function_id'] == ['Function ID %s already exists.' % function.function_id]


@pytest.mark.django_db
def test_function_put_invalid_attributes(function_data, user_api_client, function):
    function_data['function_id'] = function.function_id
    function_data['attributes'] = {'InvalidFunctionAttribute': 'value'}
    function_data['phases'][0]['attributes'] = {'InvalidPhaseAttribute': 'value'}

    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 400
    assert response.data['attributes']['InvalidFunctionAttribute'] == ['Invalid attribute.']
    assert response.data['phases'][0]['attributes']['InvalidPhaseAttribute'] == ['Invalid attribute.']
