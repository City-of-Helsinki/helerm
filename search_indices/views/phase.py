from search_indices.backends.faceted_attribute_backend import FacetedAttributeBackend
from search_indices.documents.phase import PhaseDocument
from search_indices.serializers.phase import PhaseSearchSerializer
from search_indices.views.base import BaseSearchDocumentViewSet
from search_indices.views.utils import populate_filter_fields_with_attributes


class PhaseSearchDocumentViewSet(BaseSearchDocumentViewSet):
    document = PhaseDocument
    serializer_class = PhaseSearchSerializer

    filter_fields = {}
    base_attributes = FacetedAttributeBackend.get_attributes([PhaseDocument])
    populate_filter_fields_with_attributes(filter_fields, base_attributes)

    base_search_fields = tuple(
        f"attributes.phase_{attribute}" for attribute in base_attributes
    )
