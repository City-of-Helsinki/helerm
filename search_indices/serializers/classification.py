from search_indices.documents import ClassificationDocument
from search_indices.serializers.base import BaseSearchSerializer


class ClassificationSearchSerializer(BaseSearchSerializer):
    class Meta:
        document = ClassificationDocument
