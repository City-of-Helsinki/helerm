import pytest
from rest_framework.reverse import reverse


@pytest.fixture
def attribute(choice_attribute):
    return choice_attribute


@pytest.mark.parametrize('resource', [
    'function',
    'phase',
    'action',
    'record',
    'attribute',
    'record_type'
])
@pytest.mark.django_db
def test_get(client, resource, function, phase, action, record, attribute, record_type):
    """
    Test GET to every resource's list and detail endpoint.
    """
    list_url = reverse('v1:%s-list' % resource.replace('_', ''))
    response = client.get(list_url)
    assert response.status_code == 200
    assert len(response.data['results'])

    detail_url = reverse('v1:%s-detail' % resource.replace('_', ''), kwargs={'pk': locals().get(resource).id})
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
