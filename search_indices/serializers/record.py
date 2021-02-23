from search_indices.documents import RecordDocument
from search_indices.serializers.base import BaseSearchSerializer


class RecordSearchSerializer(BaseSearchSerializer):
    class Meta:
        document = RecordDocument
