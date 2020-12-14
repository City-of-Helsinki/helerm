from search_indices.backends.faceted_attribute_backend import FacetedAttributeBackend
from search_indices.documents.action import ActionDocument
from search_indices.serializers.action import ActionSearchSerializer
from search_indices.views.base import BaseSearchDocumentViewSet
from search_indices.views.utils import populate_filter_fields_with_attributes


class ActionSearchDocumentViewSet(BaseSearchDocumentViewSet):
    document = ActionDocument
    serializer_class = ActionSearchSerializer

    filter_fields = {}
    attributes = FacetedAttributeBackend.get_attributes([ActionDocument])
    populate_filter_fields_with_attributes(filter_fields, attributes)

    search_fields = tuple(f"attributes.{attribute}" for attribute in attributes)
