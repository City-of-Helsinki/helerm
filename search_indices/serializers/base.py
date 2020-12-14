from typing import Optional

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from elasticsearch_dsl.response.hit import Hit
from rest_framework import serializers

from search_indices.serializers.utils import get_attributes


class BaseSearchSerializer(DocumentSerializer):
    attributes = serializers.SerializerMethodField()

    score = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "title",
            "description",
            "description_internal",
            "additional_information",
            "state",
            "code",
            "type",
            "parent",
            "attributes",
            "score",
        )

    def get_score(self, obj: Hit) -> int:
        return obj.meta.score

    def get_attributes(self, obj: Hit) -> Optional[dict]:
        return get_attributes(obj, "attributes")
