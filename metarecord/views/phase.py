from rest_framework import serializers, viewsets

from metarecord.models import Phase

from .action import ActionDetailSerializer
from .base import DetailSerializerMixin, HexRelatedField, StructuralElementSerializer


class PhaseListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Phase

    name = serializers.CharField(read_only=True, source='get_name')
    function = HexRelatedField(read_only=True)
    actions = HexRelatedField(many=True, read_only=True)


class PhaseDetailSerializer(PhaseListSerializer):
    actions = ActionDetailSerializer(many=True)

    class Meta(PhaseListSerializer.Meta):
        read_only_fields = ('index',)


class PhaseViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Phase.objects.prefetch_related('actions')
    serializer_class = PhaseListSerializer
    serializer_class_detail = PhaseDetailSerializer
    lookup_field = 'uuid'
