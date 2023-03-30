from django.conf import settings
from django_elasticsearch_dsl import Index

import search_indices
from metarecord.models import Action
from search_indices.documents.base import BaseDocument

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

INDEX.analyzer(search_indices.FINNISH_ANALYZER)

INDEX.settings(
    max_result_window=500000,
)


@INDEX.document
class ActionDocument(BaseDocument):
    class Django:
        model = Action
