from django.conf import settings
from elasticsearch_dsl import Search

from search_indices.documents.action import ActionDocument
from search_indices.serializers.action import ActionSearchSerializer
from search_indices.views.base import BaseSearchDocumentViewSet


class AllSearchDocumentViewSet(BaseSearchDocumentViewSet):
    document = ActionDocument  # This needs to be filled with a valid Document
    serializer_class = (
        ActionSearchSerializer  # This needs to be filled with a valid Serializer
    )

    def __init__(self, *args, **kwargs):
        super(AllSearchDocumentViewSet, self).__init__(*args, **kwargs)

        self.search = Search(
            using=self.client,
            index=list(settings.ELASTICSEARCH_INDEX_NAMES.values()),
            doc_type=self.document._doc_type.name,
        ).sort(*self.ordering)
        self.search.params(preserve_order=False)
