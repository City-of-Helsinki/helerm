from elasticsearch.helpers.test import get_test_client
from elasticsearch_dsl.connections import add_connection
from pytest import fixture

from metarecord.models import Action, Classification, Function, Phase, Record
from metarecord.tests.conftest import user, user_api_client  # noqa
from search_indices.documents import (
    ActionDocument,
    ClassificationDocument,
    FunctionDocument,
    PhaseDocument,
    RecordDocument,
)


def destroy_indices():
    ActionDocument._index.delete(ignore=[400, 404])
    ClassificationDocument._index.delete(ignore=[400, 404])
    FunctionDocument._index.delete(ignore=[400, 404])
    PhaseDocument._index.delete(ignore=[400, 404])
    RecordDocument._index.delete(ignore=[400, 404])


@fixture(scope="session", autouse=True)
def create_indices():
    """
    Initialize all indices with the custom analyzers.
    """
    destroy_indices()

    ActionDocument._index.create(ignore=[400, 404])
    ClassificationDocument._index.create(ignore=[400, 404])
    FunctionDocument._index.create(ignore=[400, 404])
    PhaseDocument._index.create(ignore=[400, 404])
    RecordDocument._index.create(ignore=[400, 404])

    yield

    destroy_indices()


@fixture(scope="session")
def es_connection():
    es_connection = get_test_client()
    add_connection("default", es_connection)
    yield es_connection


@fixture
def action(phase):
    return Action.objects.create(
        attributes={"AdditionalInformation": "testisana"}, phase=phase, index=1
    )


@fixture
def classification():
    return Classification.objects.create(
        title="testisana",
        code="00 00",
        state=Classification.APPROVED,
        function_allowed=True,
    )


@fixture
def classification2():
    return Classification.objects.create(
        title="testisana ja toinen testisana",
        code="00 00",
        state=Classification.APPROVED,
        function_allowed=True,
    )


@fixture
def function(classification):
    return Function.objects.create(
        attributes={"AdditionalInformation": "testisana"},
        classification=classification,
    )


@fixture
def phase(function):
    return Phase.objects.create(
        attributes={"AdditionalInformation": "testisana"}, function=function, index=1
    )


@fixture
def record(action):
    return Record.objects.create(
        attributes={"AdditionalInformation": "testisana"}, action=action, index=1
    )
