import pytest
from rest_framework.reverse import reverse

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
def test_classification_search_query_string(user_api_client, classification2):
    url = ALL_LIST_URL + '?search_simple_query_string="testisana ja toinen testisana"'
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert classification2.uuid.hex in uuids


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
def test_record_filter_attribute_exact(user_api_client, record):
    url = RECORD_LIST_URL + "?record_AdditionalInformation=testisana"
    response = user_api_client.get(url)
    assert response.status_code == 200

    results = response.data["results"] if "results" in response.data else response.data
    uuids = list(result["id"] for result in results)
    assert record.uuid.hex in uuids
