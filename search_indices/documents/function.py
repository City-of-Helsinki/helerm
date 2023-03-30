from django.conf import settings
from django.db.models import QuerySet
from django_elasticsearch_dsl import Index

import search_indices
from metarecord.models import Function
from search_indices.documents.base import BaseDocument

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])


INDEX.analyzer(search_indices.FINNISH_ANALYZER)

INDEX.settings(
    max_result_window=500000,
)


@INDEX.document
class FunctionDocument(BaseDocument):
    class Django:
        model = Function

    def get_queryset(self) -> QuerySet:
        return Function.objects.latest_version()
