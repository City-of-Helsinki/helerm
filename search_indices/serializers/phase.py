from search_indices.documents import PhaseDocument
from search_indices.serializers.base import BaseSearchSerializer


class PhaseSearchSerializer(BaseSearchSerializer):
    class Meta:
        document = PhaseDocument
