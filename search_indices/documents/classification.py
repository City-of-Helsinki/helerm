from django.conf import settings
from django.db.models import QuerySet
from django_elasticsearch_dsl import Index

from metarecord.models import Classification
from search_indices import get_finnish_analyzer
from search_indices.documents.base import BaseDocument

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

finnish_analyzer = get_finnish_analyzer()

INDEX.analyzer(finnish_analyzer)

INDEX.settings(
    max_result_window=500000,
)


@INDEX.document
class ClassificationDocument(BaseDocument):
    class Django:
        model = Classification

    def get_queryset(self) -> QuerySet:
        return Classification.objects.latest_version()
