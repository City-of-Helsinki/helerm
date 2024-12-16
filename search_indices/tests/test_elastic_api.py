import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from metarecord.models import Record

ACTION_LIST_URL = reverse("action_search-list")
ALL_LIST_URL = reverse("all_search-list")
CLASSIFICATION_LIST_URL = reverse("classification_search-list")
FUNCTION_LIST_URL = reverse("function_search-list")
PHASE_LIST_URL = reverse("phase_search-list")
RECORD_LIST_URL = reverse("record_search-list")


@pytest.mark.django_db
def test_classification_search_exact(user_api_client, classification):
    url = ALL_LIST_URL + "?search=testisana"
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert classification.uuid.hex in uuids


@pytest.mark.django_db
def test_classification_search_fuzzy1(user_api_client, classification):
    url = ALL_LIST_URL + "?search=testi"
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert classification.uuid.hex in uuids


@pytest.mark.django_db
def test_classification_search_fuzzy2(user_api_client, classification):
    url = ALL_LIST_URL + "?search=testisanojat"
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert classification.uuid.hex in uuids


@pytest.mark.django_db
def test_classification_search_query_string(user_api_client, classification_2):
    url = ALL_LIST_URL + '?search_simple_query_string="testisana ja toinen testisana"'
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert classification_2.uuid.hex in uuids


@pytest.mark.django_db
def test_action_filter_attribute_exact(user_api_client, action):
    url = ACTION_LIST_URL + "?action_AdditionalInformation=testisana"
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert action.uuid.hex in uuids


@pytest.mark.django_db
def test_classification_filter_title_exact(user_api_client, classification):
    url = CLASSIFICATION_LIST_URL + "?title=testisana"
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert classification.uuid.hex in uuids


@pytest.mark.django_db
def test_function_filter_attribute_exact(user_api_client, function):
    url = FUNCTION_LIST_URL + "?function_AdditionalInformation=testisana"
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert function.uuid.hex in uuids


@pytest.mark.django_db
def test_phase_filter_attribute_exact(user_api_client, phase):
    url = PHASE_LIST_URL + "?phase_AdditionalInformation=testisana"
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert phase.uuid.hex in uuids


@pytest.mark.django_db
def test_record_filter_attribute_exact(user_api_client, record, record_2):
    assert Record.objects.count() == 2

    url = RECORD_LIST_URL + "?record_AdditionalInformation=testisana"
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert len(results) == 1
    assert record.uuid.hex in uuids
    assert record_2.uuid.hex not in uuids


@pytest.mark.django_db
def test_record_filter_information_system_attribute_exact_filters_for_authenticated(
    user_api_client, record_with_information_system, record_2
):
    assert Record.objects.count() == 2

    url = RECORD_LIST_URL + "?record_InformationSystem=xyz"
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert record_with_information_system.uuid.hex in uuids
    assert record_2.uuid.hex not in uuids


@pytest.mark.django_db
def test_record_filter_information_system_attribute_exact_does_not_filter_for_unauthenticated(
    record_with_information_system, record_2
):
    assert Record.objects.count() == 2

    url = RECORD_LIST_URL + "?record_InformationSystem=xyz"
    api_client = APIClient()
    response = api_client.get(url)

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert response.status_code == 200
    assert record_with_information_system.uuid.hex in uuids
    assert record_2.uuid.hex in uuids
