"""
Regression tests for N+1 query bugs (Sentry: TIEDONOHJAUS-API N+1 Query issues).

Each test asserts that an endpoint's query count stays constant as the amount of
data it returns grows. Before the fixes these counts grew linearly with the data.
"""

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from rest_framework.reverse import reverse

from metarecord.models import (
    Action,
    Attribute,
    AttributeValue,
    Function,
    Phase,
    Record,
)

ATTRIBUTE_SCHEMAS_URL = reverse("attribute-schemas")


# The hardcoded validations require attributes these tests don't create.
@pytest.fixture(autouse=True)
def disable_attribute_validations(monkeypatch):
    for structural_element in (Function, Phase, Action, Record):
        monkeypatch.setattr(
            structural_element,
            "_attribute_validations",
            dict.fromkeys(structural_element._attribute_validations),
        )


@pytest.fixture
def count_queries():
    """Return a callable giving the number of queries a successful GET makes."""

    def _count(api_client, url):
        api_client.get(url)  # warm up caches that are populated on first use

        with CaptureQueriesContext(connection) as queries:
            response = api_client.get(url)

        assert response.status_code == 200
        return len(queries)

    return _count


@pytest.mark.django_db
def test_attribute_schemas_query_count_is_independent_of_attribute_count(
    api_client, count_queries, choice_attribute, choice_value_1
):
    baseline = count_queries(api_client, ATTRIBUTE_SCHEMAS_URL)

    for index in range(4):
        attribute = Attribute.objects.create(
            name=f"extra attribute {index}", identifier=f"ExtraAttr{index}"
        )
        AttributeValue.objects.create(attribute=attribute, value=f"value {index}")

    assert count_queries(api_client, ATTRIBUTE_SCHEMAS_URL) == baseline


@pytest.mark.django_db
def test_function_detail_query_count_is_independent_of_phase_count(
    user_api_client, count_queries, function, record
):
    url = reverse("function-detail", kwargs={"uuid": function.uuid})
    baseline = count_queries(user_api_client, url)

    for index in range(2, 6):
        phase = Phase.objects.create(function=function, index=index)
        action = Action.objects.create(phase=phase, index=index)
        Record.objects.create(action=action, index=index)

    assert count_queries(user_api_client, url) == baseline
