from rest_framework import viewsets

from metarecord.models import Action

from .base import DetailSerializerMixin, HexRelatedField, StructuralElementSerializer
from .record import RecordDetailSerializer


class ActionListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Action

    phase = HexRelatedField(read_only=True, )
    records = HexRelatedField(many=True, read_only=True)


class ActionDetailSerializer(ActionListSerializer):
    records = RecordDetailSerializer(many=True)


class ActionViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.prefetch_related('records')
    serializer_class = ActionListSerializer
    serializer_class_detail = ActionDetailSerializer
    lookup_field = 'uuid'
