from search_indices.backends.faceted_attribute_backend import FacetedAttributeBackend
from search_indices.documents.record import RecordDocument
from search_indices.serializers.record import RecordSearchSerializer
from search_indices.views.base import BaseSearchDocumentViewSet
from search_indices.views.utils import populate_filter_fields_with_attributes


class RecordSearchDocumentViewSet(BaseSearchDocumentViewSet):
    document = RecordDocument
    serializer_class = RecordSearchSerializer

    filter_fields = {}
    attributes = FacetedAttributeBackend.get_attributes([RecordDocument])
    populate_filter_fields_with_attributes(filter_fields, attributes)

    search_fields = tuple(f"attributes.{attribute}" for attribute in attributes)
