from search_indices.documents.classification import ClassificationDocument
from search_indices.serializers.classification import ClassificationSearchSerializer
from search_indices.views.base import BaseSearchDocumentViewSet


class ClassificationSearchDocumentViewSet(BaseSearchDocumentViewSet):
    document = ClassificationDocument
    serializer_class = ClassificationSearchSerializer

    filter_fields = {
        "title": "title",
        "description": "description",
        "related_classification": "related_classification",
        "internal_description": "internal_description",
        "additional_information": "additional_information",
    }

    base_search_fields = (
        "title",
        "description",
        "related_classification",
        "internal_description",
        "additional_information",
    )
