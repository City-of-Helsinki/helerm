from search_indices.documents import FunctionDocument
from search_indices.serializers.base import BaseSearchSerializer


class FunctionSearchSerializer(BaseSearchSerializer):
    class Meta:
        document = FunctionDocument
