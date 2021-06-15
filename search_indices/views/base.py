from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend, FacetedSearchFilterBackend, FilteringFilterBackend,
    SimpleQueryStringSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet

from metarecord.pagination import ESRecordPagination
from search_indices.backends.faceted_attribute_backend import FacetedAttributeBackend
from search_indices.views.utils import populate_filter_fields_with_attributes


class BaseSearchDocumentViewSet(BaseDocumentViewSet):
    pagination_class = ESRecordPagination
    lookup_field = "id"
    filter_backends = [
        CompoundSearchFilterBackend,
        FacetedAttributeBackend,
        FacetedSearchFilterBackend,
        FilteringFilterBackend,
        SimpleQueryStringSearchFilterBackend,
    ]

    faceted_search_fields = {
        "title": {
            "field": "title.keyword",
            "enabled": True,
        },
        "description": {
            "field": "description.keyword",
            "enabled": True,
        },
        "related_classification": {
            "field": "related_classification.keyword",
            "enabled": True,
        },
        "internal_description": {
            "field": "internal_description.keyword",
            "enabled": True,
        },
        "additional_information": {
            "field": "additional_information.keyword",
            "enabled": True,
        },
        "type": {
            "field": "type",
            "enabled": True,
        },
    }

    filter_fields = {}
    attributes = FacetedAttributeBackend.get_attributes()
    populate_filter_fields_with_attributes(filter_fields, attributes)

    search_fields = (
        "title",
        "description",
        "related_classification",
        "internal_description",
        "additional_information",
    )

    search_fields += tuple(f"attributes.{attribute}" for attribute in attributes)

    ordering = (
        "type",
        "_score",
    )
