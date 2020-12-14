from search_indices.documents import ActionDocument
from search_indices.serializers.base import BaseSearchSerializer


class ActionSearchSerializer(BaseSearchSerializer):
    class Meta:
        document = ActionDocument
