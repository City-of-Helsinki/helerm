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
    'record_attachment',
    'attribute'
])
@pytest.mark.django_db
def test_get(client, resource, function, phase, action, record, record_attachment, attribute):
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
