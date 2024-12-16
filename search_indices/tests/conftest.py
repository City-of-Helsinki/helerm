import os
import time
from os.path import abspath, dirname, join
from unittest import SkipTest

from django.conf import settings
from elasticsearch import Elasticsearch
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

# The tests rely on elasticsearch.helpers.test, which was removed in elasticsearch-py 8.0.
# Copied from https://github.com/elastic/elasticsearch-py/commit/3a44a501b4dbc9fed897a7fd1c70aad881d6944f#diff-fbe7638e315bad1693000e7e7c7a22f19b14e9a709d39996bac8fc8ae26916d8L33-L58  # noqa: E501

CA_CERTS = join(dirname(dirname(dirname(abspath(__file__)))), ".ci/certs/ca.pem")


def get_test_client(nowait=False, **kwargs):
    # construct kwargs from the environment
    kw = {"timeout": 30, "ca_certs": CA_CERTS}
    if "PYTHON_CONNECTION_CLASS" in os.environ:
        from elasticsearch import connection

        kw["connection_class"] = getattr(
            connection, os.environ["PYTHON_CONNECTION_CLASS"]
        )

    kw.update(kwargs)
    client = Elasticsearch(settings.ELASTICSEARCH_URL, **kw)

    # wait for yellow status
    for _ in range(1 if nowait else 100):
        try:
            client.cluster.health(wait_for_status="yellow")
            return client
        except ConnectionError:
            time.sleep(0.1)
    else:
        # timeout
        raise SkipTest("Elasticsearch failed to start.")


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
def action_2(phase_2):
    return Action.objects.create(
        attributes={"AdditionalInformation": "testisana"}, phase=phase_2, index=1
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
def classification_2():
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
def function_2(classification_2):
    return Function.objects.create(
        attributes={"AdditionalInformation": "testword"},
        classification=classification_2,
    )


@fixture
def phase(function):
    return Phase.objects.create(
        attributes={"AdditionalInformation": "testisana"}, function=function, index=1
    )


@fixture
def phase_2(function_2):
    return Phase.objects.create(
        attributes={"AdditionalInformation": "testword"}, function=function_2, index=1
    )


@fixture
def record(action):
    return Record.objects.create(
        attributes={"AdditionalInformation": "testisana"}, action=action, index=1
    )


@fixture
def record_with_information_system(action):
    return Record.objects.create(
        attributes={"InformationSystem": "xyz"}, action=action, index=1
    )


@fixture
def record_2(action_2):
    return Record.objects.create(
        attributes={"AdditionalInformation": "testword"}, action=action_2, index=1
    )
