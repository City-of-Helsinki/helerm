from search_indices.backends.faceted_attribute_backend import FacetedAttributeBackend
from search_indices.documents.function import FunctionDocument
from search_indices.serializers.function import FunctionSearchSerializer
from search_indices.views.base import BaseSearchDocumentViewSet
from search_indices.views.utils import populate_filter_fields_with_attributes


class FunctionSearchDocumentViewSet(BaseSearchDocumentViewSet):
    document = FunctionDocument
    serializer_class = FunctionSearchSerializer

    filter_fields = {}
    base_attributes = FacetedAttributeBackend.get_attributes([FunctionDocument])
    populate_filter_fields_with_attributes(filter_fields, base_attributes)

    base_search_fields = tuple(
        f"attributes.{attribute}" for attribute in base_attributes
    )
