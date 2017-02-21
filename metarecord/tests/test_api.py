import pytest
from rest_framework.reverse import reverse
from metarecord.models import Function


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
def test_get(client, resource, function, phase, action, record, attribute, template):
    """
    Test GET to every resource's list and detail endpoint.
    """
    list_url = reverse('v1:%s-list' % resource)
    response = client.get(list_url)
    assert response.status_code == 200
    assert len(response.data['results'])

    id_field = 'pk' if resource is 'attribute' else 'uuid'
    id_value = getattr(locals().get(resource), id_field)
    detail_url = reverse('v1:%s-detail' % resource.replace('_', ''), kwargs={id_field: id_value})
    response = client.get(detail_url)
    assert response.status_code == 200
    assert response.data


@pytest.mark.django_db
def test_get_attribute_schemas(client):
    url = '{}schemas/'.format(reverse('v1:attribute-list'))
    response = client.get(url)
    assert response.status_code == 200

    for element in ('function', 'phase', 'action', 'record'):
        assert len(response.data.get(element))


@pytest.mark.django_db
def test_function_versioning(client):
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
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == 'second draft'

    # /function/<uuid>/?state=approved should return the latest approved version
    response = client.get(url + '?state=approved')
    assert response.status_code == 200
    assert response.data['name'] == 'second approved'
