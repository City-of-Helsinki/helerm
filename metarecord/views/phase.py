from rest_framework import viewsets

from metarecord.models import Phase

from .action import ActionDetailSerializer
from .base import AttributeFilter, DetailSerializerMixin, HexPrimaryKeyRelatedField, StructuralElementSerializer


class PhaseListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Phase

    function = HexPrimaryKeyRelatedField(read_only=True, source='function_id')
    actions = HexPrimaryKeyRelatedField(many=True, read_only=True)


class PhaseDetailSerializer(PhaseListSerializer):
    actions = ActionDetailSerializer(many=True)


class PhaseViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Phase.objects.all()
    serializer_class = PhaseListSerializer
    serializer_class_detail = PhaseDetailSerializer
    filter_backends = (AttributeFilter,)
