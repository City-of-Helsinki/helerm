import pytest
from rest_framework.reverse import reverse

from metarecord.models import Phase, Record

ACTION_LIST_URL = reverse("action_search-list")
ALL_LIST_URL = reverse("all_search-list")
CLASSIFICATION_LIST_URL = reverse("classification_search-list")
FUNCTION_LIST_URL = reverse("function_search-list")
PHASE_LIST_URL = reverse("phase_search-list")
RECORD_LIST_URL = reverse("record_search-list")


@pytest.mark.django_db
class TestClassificationSearch:
    def test_classification_search_exact(self, user_api_client, classification):
        url = ALL_LIST_URL + "?search=testisana"
        response = user_api_client.get(url)
        assert response.status_code == 200

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert classification.uuid.hex in uuids

    def test_classification_search_fuzzy1(self, user_api_client, classification):
        url = ALL_LIST_URL + "?search=testi"
        response = user_api_client.get(url)
        assert response.status_code == 200

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert classification.uuid.hex in uuids

    def test_classification_search_fuzzy2(self, user_api_client, classification):
        url = ALL_LIST_URL + "?search=testisanojat"
        response = user_api_client.get(url)
        assert response.status_code == 200

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert classification.uuid.hex in uuids

    def test_classification_search_query_string(
        self, user_api_client, classification_2
    ):
        url = (
            ALL_LIST_URL + '?search_simple_query_string="testisana ja toinen testisana"'
        )
        response = user_api_client.get(url)
        assert response.status_code == 200

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert classification_2.uuid.hex in uuids


@pytest.mark.django_db
class TestListFilters:
    def test_classification_filter_title_exact(self, user_api_client, classification):
        url = CLASSIFICATION_LIST_URL + "?title=testisana"
        response = user_api_client.get(url)
        assert response.status_code == 200

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert classification.uuid.hex in uuids

    def test_action_filter_attribute_exact(self, user_api_client, action):
        url = ACTION_LIST_URL + "?action_AdditionalInformation=testisana"
        response = user_api_client.get(url)
        assert response.status_code == 200

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert action.uuid.hex in uuids

    def test_function_filter_attribute_exact(self, user_api_client, function):
        url = FUNCTION_LIST_URL + "?function_AdditionalInformation=testisana"
        response = user_api_client.get(url)
        assert response.status_code == 200

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert function.uuid.hex in uuids

    def test_phase_filter_attribute_exact(self, user_api_client, phase):
        url = PHASE_LIST_URL + "?phase_AdditionalInformation=testisana"
        response = user_api_client.get(url)
        assert response.status_code == 200

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert phase.uuid.hex in uuids

    def test_record_filter_attribute_exact(self, user_api_client, record, record_2):
        assert Record.objects.count() == 2

        url = RECORD_LIST_URL + "?record_AdditionalInformation=testisana"
        response = user_api_client.get(url)
        assert response.status_code == 200

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert len(results) == 1
        assert record.uuid.hex in uuids
        assert record_2.uuid.hex not in uuids


@pytest.mark.django_db
class TestFunctionAllSearchInformationSystem:
    def test_not_match_for_unauthenticated(
        self, api_client, function_with_information_system, phase
    ):
        phase.attributes = {"AdditionalInformation": "xyz"}
        phase.save()

        response = api_client.get(ALL_LIST_URL + "?search=xyz")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)

        assert function_with_information_system.uuid.hex not in uuids
        assert phase.uuid.hex in uuids

    def test_information_system_not_visible_for_unauthenticated(
        self, api_client, function_with_information_system, phase
    ):
        phase.attributes = {"AdditionalInformation": "testing"}
        phase.save()
        function_with_information_system.attributes = {
            "InformationSystem": "xyz",
            "AdditionalInformation": "testing",
        }
        function_with_information_system.save()

        response = api_client.get(ALL_LIST_URL + "?search=testing")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)

        assert function_with_information_system.uuid.hex in uuids
        assert phase.uuid.hex in uuids
        assert {"function_InformationSystem": "xyz"} not in attributes

    def test_information_system_is_visible_for_authenticated(
        self, user_api_client, function_with_information_system, phase
    ):
        response = user_api_client.get(ALL_LIST_URL + "?search=xyz")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)

        assert function_with_information_system.uuid.hex in uuids
        assert phase.uuid.hex not in uuids
        assert {"function_InformationSystem": "xyz"} in attributes


@pytest.mark.django_db
class TestActionAllSearchInformationSystem:
    def test_not_match_for_unauthenticated(
        self, api_client, action_with_information_system, function_2
    ):
        function_2.attributes = {"AdditionalInformation": "xyz"}
        function_2.save()

        response = api_client.get(ALL_LIST_URL + "?search=xyz")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)

        assert action_with_information_system.uuid.hex not in uuids
        assert function_2.uuid.hex in uuids

    def test_information_system_not_visible_for_unauthenticated(
        self, api_client, action_with_information_system, function_2
    ):
        function_2.attributes = {"AdditionalInformation": "testing"}
        function_2.save()
        action_with_information_system.attributes = {
            "InformationSystem": "xyz",
            "AdditionalInformation": "testing",
        }
        action_with_information_system.save()

        response = api_client.get(ALL_LIST_URL + "?search=testing")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)

        assert action_with_information_system.uuid.hex in uuids
        assert function_2.uuid.hex in uuids
        assert {"action_InformationSystem": "xyz"} not in attributes

    def test_information_system_is_visible_for_authenticated(
        self, user_api_client, action_with_information_system, function_2
    ):
        response = user_api_client.get(ALL_LIST_URL + "?search=xyz")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)
        assert action_with_information_system.uuid.hex in uuids
        assert function_2.uuid.hex not in uuids
        assert {"action_InformationSystem": "xyz"} in attributes


@pytest.mark.django_db
class TestRecordAllSearchInformationSystem:
    def test_not_match_for_unauthenticated(
        self, api_client, record_with_information_system, function_2
    ):
        function_2.attributes = {"AdditionalInformation": "xyz"}
        function_2.save()

        response = api_client.get(ALL_LIST_URL + "?search=xyz")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)

        assert record_with_information_system.uuid.hex not in uuids
        assert function_2.uuid.hex in uuids

    def test_information_system_not_visible_for_unauthenticated(
        self, api_client, record_with_information_system, function_2
    ):
        function_2.attributes = {"AdditionalInformation": "testing"}
        function_2.save()
        record_with_information_system.attributes = {
            "InformationSystem": "xyz",
            "AdditionalInformation": "testing",
        }
        record_with_information_system.save()

        response = api_client.get(ALL_LIST_URL + "?search=testing")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)

        assert record_with_information_system.uuid.hex in uuids
        assert function_2.uuid.hex in uuids
        assert {"action_InformationSystem": "xyz"} not in attributes

    def test_information_system_is_visible_for_authenticated(
        self, user_api_client, record_with_information_system, function_2
    ):
        response = user_api_client.get(ALL_LIST_URL + "?search=xyz")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)
        assert record_with_information_system.uuid.hex in uuids
        assert function_2.uuid.hex not in uuids
        assert {"record_InformationSystem": "xyz"} in attributes


@pytest.mark.django_db
class TestPhaseAllSearchInformationSystem:
    def test_not_match_for_unauthenticated(
        self, api_client, phase_with_information_system, function_2
    ):
        function_2.attributes = {"AdditionalInformation": "xyz"}
        function_2.save()

        response = api_client.get(ALL_LIST_URL + "?search=xyz")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)

        assert phase_with_information_system.uuid.hex not in uuids
        assert function_2.uuid.hex in uuids

    def test_information_system_not_visible_for_unauthenticated(
        self, api_client, phase_with_information_system, function_2
    ):
        function_2.attributes = {"AdditionalInformation": "testing"}
        function_2.save()
        phase_with_information_system.attributes = {
            "InformationSystem": "xyz",
            "AdditionalInformation": "testing",
        }
        phase_with_information_system.save()

        response = api_client.get(ALL_LIST_URL + "?search=testing")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)

        assert phase_with_information_system.uuid.hex in uuids
        assert function_2.uuid.hex in uuids
        assert {"action_InformationSystem": "xyz"} not in attributes

    def test_information_system_is_visible_for_authenticated(
        self, user_api_client, phase_with_information_system, function_2
    ):
        response = user_api_client.get(ALL_LIST_URL + "?search=xyz")
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)
        assert phase_with_information_system.uuid.hex in uuids
        assert function_2.uuid.hex not in uuids
        assert {"phase_InformationSystem": "xyz"} in attributes


@pytest.mark.django_db
class TestInformationSystemAttributeListUrls:
    def test_action_information_system_attribute_for_authenticated(
        self, user_api_client, action_with_information_system
    ):
        response = user_api_client.get(ACTION_LIST_URL)
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)

        assert response.status_code == 200
        assert action_with_information_system.uuid.hex in uuids
        assert {"action_InformationSystem": "xyz"} in attributes

    def test_action_does_not_show_information_system_attribute_for_unauthenticated(
        self, api_client, action_with_information_system
    ):
        response = api_client.get(ACTION_LIST_URL)

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)

        assert response.status_code == 200
        assert action_with_information_system.uuid.hex in uuids
        assert {"action_InformationSystem": "xyz"} not in attributes

    def test_record_filter_information_system_attribute_exact_filters_for_authenticated(
        self, user_api_client, record_with_information_system, record_2
    ):
        assert Record.objects.count() == 2

        url = RECORD_LIST_URL + "?record_InformationSystem=xyz"
        response = user_api_client.get(url)
        assert response.status_code == 200

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert record_with_information_system.uuid.hex in uuids
        assert record_2.uuid.hex not in uuids

    def test_record_does_shows_information_system_attribute_for_authenticated(
        self, user_api_client, record_with_information_system, record_2
    ):
        response = user_api_client.get(RECORD_LIST_URL)
        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)

        assert response.status_code == 200
        assert record_with_information_system.uuid.hex in uuids
        assert {"record_InformationSystem": "xyz"} in attributes
        assert record_2.uuid.hex in uuids

    def test_record_does_not_show_information_system_attribute_for_unauthenticated(
        self, api_client, record_with_information_system, record_2
    ):
        response = api_client.get(RECORD_LIST_URL)

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        attributes = list(result["attributes"] for result in results)

        assert response.status_code == 200
        assert record_with_information_system.uuid.hex in uuids
        assert {"record_InformationSystem": "xyz"} not in attributes
        assert record_2.uuid.hex in uuids

    def test_record_filter_information_system_attribute_exact_does_not_filter_for_unauthenticated(
        self, api_client, record_with_information_system, record_2
    ):
        assert Record.objects.count() == 2

        url = RECORD_LIST_URL + "?record_InformationSystem=xyz"
        response = api_client.get(url)

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert response.status_code == 200
        assert record_with_information_system.uuid.hex in uuids
        assert record_2.uuid.hex in uuids

    def test_phase_filter_information_system_attribute_exact_for_authenticated(
        self, user_api_client, phase_with_information_system, phase_2
    ):
        assert Phase.objects.count() == 2
        url = PHASE_LIST_URL + "?phase_InformationSystem=xyz"
        response = user_api_client.get(url)

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert response.status_code == 200
        assert phase_with_information_system.uuid.hex in uuids
        assert phase_2.uuid.hex not in uuids

    def test_phase_filter_information_system_attribute_exact_does_not_filter_for_unauthenticated(
        self, api_client, phase_with_information_system, phase_2
    ):
        assert Phase.objects.count() == 2

        url = PHASE_LIST_URL + "?phase_InformationSystem=xyz"
        response = api_client.get(url)

        results = (
            response.data["results"] if "results" in response.data else response.data
        )
        uuids = list(result["id"] for result in results)
        assert response.status_code == 200
        assert phase_with_information_system.uuid.hex in uuids
        assert phase_2.uuid.hex in uuids


@pytest.mark.django_db
@pytest.mark.parametrize(
    "list_url",
    [
        PHASE_LIST_URL,
        ACTION_LIST_URL,
        RECORD_LIST_URL,
        FUNCTION_LIST_URL,
        ALL_LIST_URL,
    ],
)
class TestInformationSystemInFacets:
    def test_list_for_authenticated(
        self,
        user_api_client,
        list_url,
    ):
        response = user_api_client.get(list_url)
        facets = response.data["facets"] if "facets" in response.data else response.data

        assert response.status_code == 200
        assert "informationsystem" in "".join([key.lower() for key in facets])

    def test_list_for_unauthenticated(
        self,
        api_client,
        list_url,
    ):
        response = api_client.get(list_url)
        facets = response.data["facets"] if "facets" in response.data else response.data

        assert response.status_code == 200
        assert "informationsystem" not in "".join([key.lower() for key in facets])
