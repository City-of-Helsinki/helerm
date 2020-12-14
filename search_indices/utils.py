from django.conf import settings
from elasticsearch_dsl import connections


def create_elasticsearch_connection():
    es_host = settings.ELASTICSEARCH_DSL["default"]["hosts"]
    return connections.create_connection(hosts=[es_host])
