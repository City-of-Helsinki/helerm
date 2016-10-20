from rest_framework import viewsets

from metarecord.models import Action

from .base import DetailSerializerMixin, HexPrimaryKeyRelatedField, StructuralElementSerializer
from .record import RecordDetailSerializer


class ActionListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Action

    phase = HexPrimaryKeyRelatedField(read_only=True, source='phase_id')
    records = HexPrimaryKeyRelatedField(many=True, read_only=True)


class ActionDetailSerializer(ActionListSerializer):
    records = RecordDetailSerializer(many=True, read_only=True)


class ActionViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.prefetch_related('records')
    serializer_class = ActionListSerializer
    serializer_class_detail = ActionDetailSerializer
