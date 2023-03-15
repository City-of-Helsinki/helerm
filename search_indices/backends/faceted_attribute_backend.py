from typing import List, Type

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl_drf.filter_backends.mixins import FilterBackendMixin
from elasticsearch_dsl.search import Search
from rest_framework.filters import BaseFilterBackend
from rest_framework.request import Request
from rest_framework.viewsets import ReadOnlyModelViewSet

from search_indices.documents import (
    ActionDocument,
    FunctionDocument,
    PhaseDocument,
    RecordDocument,
)

DOCUMENT_TYPES = [
    ActionDocument,
    FunctionDocument,
    PhaseDocument,
    RecordDocument,
]


class FacetedAttributeBackend(BaseFilterBackend, FilterBackendMixin):
    """Adds faceted search for attributes."""

    faceted_search_param = "facet_attribute"

    @staticmethod
    def get_attributes(documents: List[Type[Document]] = None) -> list:
        if not documents:
            documents = DOCUMENT_TYPES
        attrs = []
        for document in documents:
            model = document.Django.model
            attributes = getattr(model, "_attribute_validations", None)
            if attributes:
                attrs += map(
                    lambda x, model=model: f"{str(model._meta.verbose_name)}_{x}",
                    attributes["allowed"],
                )
        return attrs

    def filter_queryset(
        self, request: Request, queryset: Search, view: Type[ReadOnlyModelViewSet]
    ) -> Search:
        """Filter the queryset.
        :param request: Django REST framework request.
        :param queryset: Base queryset.
        :param view: View.
        :type request: rest_framework.request.Request
        :type queryset: elasticsearch_dsl.search.Search
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Updated queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        attribute_validations = view.attributes
        if attribute_validations:
            for attribute in attribute_validations:
                attribute_replaced = attribute.replace(".", "+")
                # Example ("_attribute_Subject.Scheme", "terms", "attributes.Subject+Scheme.keyword")
                queryset.aggs.bucket(
                    f"_attribute_{attribute}",
                    "terms",
                    field=f"attributes.{attribute_replaced}.keyword",
                )
        return queryset
